from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_url: str = 'https://api.todoist.com/api/v1'
    token: str | None = None
    inbox_id: str | None = None


test_config = Config()
