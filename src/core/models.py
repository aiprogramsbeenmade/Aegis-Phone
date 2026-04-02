from pydantic import BaseModel, Field
from typing import Optional, List

class PhoneNumberInfo(BaseModel):
    number: str
    valid: bool = False
    carrier: Optional[str] = "Unknown"
    location: Optional[str] = "Unknown"
    line_type: Optional[str] = None # mobile, landline, voip
    social_presence: List[str] = Field(default_factory=list)
    dorking_results: List[str] = Field(default_factory=list)