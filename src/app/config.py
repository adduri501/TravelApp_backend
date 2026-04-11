from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    USER_TABLE:Optional[str]
    SECRET_KEY_JWT:str
    SQLALCHEMY_DATABASE_URI:Optional[str]
    DB_SCHEMA:Optional[str]
    DB_USER:Optional[str]
    DB_PASSWORD:Optional[str]
    DB_HOST:Optional[str]
    DB_NAME:Optional[str]
    ENVIRONMENT:Optional[str]="local"
    ALGORITHM :str
    
    

    model_config = SettingsConfigDict(
            env_file=(
                "./app/config/serverbase.cfg",
                # "./config/serveroverride.cfg",
                # "./config/serverlocal.cfg",
                # f"./config/server{environ.ENVIRONMENT}.cfg",
                # "/serveroverride.cfg",
            )
        )


settings = AppSettings()

print(settings.DB_HOST)