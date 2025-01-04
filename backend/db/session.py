import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openai import OpenAI


def get_client():
    try:
        client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        return client
    except Exception as e:
        print(f"Failed to initialize AI client: {str(e)}")
        raise Exception(f"AI服务初始化失败：{str(e)}")
