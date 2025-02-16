from pydantic import BaseModel

class Settings(BaseModel):
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS:int =7
    DATABASE_URL: str = "sqlite:///./parking.db"
    EMAIL_SENDER: str = "noreply@carparkingapp.com"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "jidris64@gmail.com"
    SMTP_PASSWORD: str = "12345678"

    class Config:
        env_file = ".env"

settings = Settings()