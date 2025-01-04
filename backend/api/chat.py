from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import sys, os
from schems.Message import Message

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import get_client

router = APIRouter(prefix="/chat", tags=["chat"])


async def generate_response(client, message: Message):
    """生成流式响应"""
    try:

        history_messages = [
            {"role": "system", "content": "you are a helpful assistant"}
        ]
        history_messages.append({"role": "user", "content": message.content})

        try:
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=history_messages,
                stream=True,
                response_format={"type": "text"},
            )

            # 逐块返回响应内容
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"\n连接AI服务失败：{str(e)}\n"
            print(f"AI Service Error: {str(e)}")

    except Exception as e:
        yield f"\n生成响应时发生错误：{str(e)}\n"
        print(f"Generate Response Error: {str(e)}")


@router.post("/chat")
async def chat(message: Message, client=Depends(get_client)):
    """聊天接口"""
    print("Received message:", message.dict())
    try:
        return StreamingResponse(
            generate_response(client, message), media_type="text/event-stream"
        )
    except Exception as e:
        print("Chat Endpoint Error:", str(e))
        raise HTTPException(status_code=500, detail=f"处理请求时发生错误：{str(e)}")
