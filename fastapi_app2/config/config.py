from pydantic_settings import BaseSettings, SettingsConfigDict

class KeyCloakSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow', env_file='.env', env_file_encoding='utf-8')
    KEYCLOAK_SERVER_URL: str
    REALM_NAME: str
    CLIENT_ID: str
    SECRET_KEY: str
    REDIRECT_URL: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow', env_file='.env', env_file_encoding='utf-8')
    DEBUG: bool = True


class Configurations(KeyCloakSettings, Settings):
    pass


settings = Configurations()