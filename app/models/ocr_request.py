from pydantic import BaseModel

class OCRRequest(BaseModel):
    text: []
    keywords_dict: {}
