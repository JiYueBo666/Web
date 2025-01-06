from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import sys, os
from schems.Message import Message

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import get_client
from prompt.math_helper import math_helper_prompt

router = APIRouter(prefix="/chat", tags=["chat"])


async def generate_response(client, message: Message):
    """生成流式响应"""

    if message.scene == "math":
        prompt = math_helper_prompt
    else:
        prompt = "you are a helpful assistant"

    try:
        # 构建对话历史
        history_messages = [{"role": "system", "content": prompt}]

        # 添加历史对话记录
        if message.history:
            for hist_msg in message.history:
                history_messages.append(
                    {"role": hist_msg.role, "content": hist_msg.content}
                )

        try:
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=history_messages,  # 现在包含了完整的对话历史
                stream=True,
                response_format={"type": "text"},
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    yield f"data: {content}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: 连接AI服务失败：{str(e)}\n\n"
            print(f"AI Service Error: {str(e)}")

    except Exception as e:
        yield f"data: 生成响应时发生错误：{str(e)}\n\n"
        print(f"Generate Response Error: {str(e)}")


@router.post("/chat")
async def chat(message: Message, client=Depends(get_client)):
    """聊天接口"""
    try:
        return StreamingResponse(
            generate_response(client, message),
            media_type="text/event-stream",  # 确保设置正确的媒体类型
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲（如果使用 Nginx）
            },
        )
    except Exception as e:
        print("Chat Endpoint Error:", str(e))
        raise HTTPException(status_code=500, detail=f"处理请求时发生错误：{str(e)}")
