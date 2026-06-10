from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # WhatsApp (PyWa)
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    whatsapp_webhook_verify_token: str

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/botdb"

    # Google Calendar
    google_credentials_path: Optional[str] = None  # JSON de Service Account
    calendar_id: str = "primary"

    # Security
    secret_key: str = "cambia_esto_por_un_secreto_seguro"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 días

    # App
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()