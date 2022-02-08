from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_API_TOKEN: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
