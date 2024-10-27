from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DB_USER: str
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_HOST: str

    @property
    def DB_URI(self):
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.DB_USER,
                password=self.DB_PASS,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        )


app_settings = _Settings()