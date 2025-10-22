from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Deskbook API'
    app_version: str = '0.0.1'
    app_key: str
    db_user: str
    db_password: str
    db_url: str

    class Config:
        env_file = '.env'


settings = Settings()
