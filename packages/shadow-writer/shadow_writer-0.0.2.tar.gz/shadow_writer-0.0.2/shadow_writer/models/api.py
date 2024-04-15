from typing import List, Optional
from pydantic import BaseModel


class ReseachRequest(BaseModel):
    """Request for writing materials reseaching."""

    article_spec: str
    seo_keywords: Optional[List[str]] = None
    max_tokens: int = 100000


class ResearchResponse(BaseModel):
    """Response for writing materies reseaching."""

    data: str  # data is a string from df.to_json(orient="records")


class WritingRequest(BaseModel):
    """Request for writing article based on spec and materials."""

    article_spec: str
    seo_keywords: Optional[List[str]] = None
    background_materials: Optional[str] = None


class WritingResponse(BaseModel):
    """article content"""

    article_content: str


class EditingRequest(BaseModel):
    """Request for editing article."""

    article_content: str
    opinion: str


class EditingResponse(BaseModel):
    """Response for editing article."""

    edited_article: str
