from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    wp_base_url: str = "https://example.com"
    wp_username: str = "editor"
    wp_app_password: str = ""
    wp_author_id: int = 1
    wp_default_status: str = "draft"
    wp_timeout: float = 30.0

    llm_provider: str = "ollama"
    ollama_host: str = "http://127.0.0.1:11434"
    ollama_model: str = "gemma2:9b-instruct-q4_K_M"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2500
    llm_timeout: float = 180.0

    memory_db: str = str(ROOT / "data" / "editorial.sqlite")
    embed_model: str = "nomic-embed-text"
    dedup_min_score: float = 0.78

    api_host: str = "127.0.0.1"
    api_port: int = 8787
    api_token: str = ""
    api_rate_limit: int = 20

    satira_email_enabled: bool = False
    imap_host: str = ""
    imap_port: int = 993
    imap_user: str = ""
    imap_password: str = ""
    imap_folder: str = "INBOX"
    imap_subject_prefix: str = "[SATIRA]"

    log_level: str = "INFO"
    log_file: str = str(ROOT / "logs" / "satira.log")


settings = Settings()
