from pydantic import BaseModel
from typing import List, Dict, Any

class OCRRequest(BaseModel):
    text: List[str]
    keywords_dict: Dict[str, Any]  # Allows mixed value types
