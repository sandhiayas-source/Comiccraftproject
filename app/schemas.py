from typing import Optional, List
from pydantic import BaseModel, Field

class ComicRequest(BaseModel):
    title: str = "Milo the Brave Little Fox"
    character: str = "Milo (Fox)"
    setting: str = "Village & Enchanted Forest"
    tone: str = "Warm and funny"
    art_style: str = "Colorful Comic Book"
    pages: int = Field(default=5, ge=3, le=8)
    use_ai: bool = True

class ComicPage(BaseModel):
    page_number: int
    title: str
    description: str
    dialogue: str
    image_url: Optional[str] = None

class ComicResponse(BaseModel):
    title: str
    tagline: str
    pages: List[ComicPage]
    moral: str
