from typing import Optional
from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: str = Field(..., min_length=2, max_length=12000)
    dates: str = Field(..., min_length=2, max_length=500)

    jurisdiction: Optional[str] = Field(
        default=None,
        max_length=200
    )

    additional_instructions: Optional[str] = Field(
        default=None,
        max_length=5000
    )

    brand_name: Optional[str] = Field(
        default=None,
        max_length=200
    )


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    mode: str
    warning: str