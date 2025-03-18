import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Chỉ load .env khi chạy local (không chạy trong Docker)
if not os.environ.get("DOCKER_ENV"):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ENV_PATH = os.path.join(BASE_DIR, ".env")
    print(ENV_PATH)
    if os.path.exists(ENV_PATH):
        print(f"🔹 Loading environment variables from: {ENV_PATH}")
        load_dotenv(ENV_PATH)
    else:
        print("⚠️ Không tìm thấy tệp .env, sử dụng giá trị mặc định!")

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    APP_NANE: str =  'FastAPIApp'
    DEBUG: bool = True
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
