from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = "your-api-key-here"  # 替换为您的实际 API key
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
