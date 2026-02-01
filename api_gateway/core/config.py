from pydantic import BaseSettings

class AuthSettings(BaseSettings):
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

auth_settings = AuthSettings()