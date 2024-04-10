from pydantic import BaseModel


class WatsonSetting(BaseModel):
    engine: str
    apikey: str
    region: str
    base_model: str
    # TODO: currently language_customization_id and acoustic_customization_id are not used
    language_customization_id: str = None
    acoustic_customization_id: str = None
