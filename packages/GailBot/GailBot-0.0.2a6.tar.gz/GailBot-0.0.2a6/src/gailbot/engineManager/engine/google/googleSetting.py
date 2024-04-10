from pydantic import BaseModel


class GoogleSetting(BaseModel):
    engine: str
    google_api_key: str
