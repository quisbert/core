from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_env: str

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    max_login_attempts: int

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    core_schema: str
    domain_schema: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )


settings = Settings()