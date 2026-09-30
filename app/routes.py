from fastapi import APIRouter, HTTPException
from app.schemas import ComicRequest, ComicResponse
from app.services.story_service import generate_story
from app.services.image_service import generate_page_image
from app.services.exporters import create_pdf
from app.utils.paths import ensure_directories

router = APIRouter(prefix="/api")
ensure_directories()

@router.post("/story/generate", response_model=ComicResponse)
def story_generate(request: ComicRequest):
    try:
        return generate_story(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/comic/generate", response_model=ComicResponse)
def comic_generate(request: ComicRequest):
    try:
        comic = generate_story(request)
        for page in comic.pages:
            page.image_url = generate_page_image(
                title=page.title,
                description=page.description,
                dialogue=page.dialogue,
                character=request.character,
                art_style=request.art_style,
                page_number=page.page_number,
            )
        return comic
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.post("/comic/pdf")
def comic_pdf(comic: ComicResponse):
    try:
        return {"pdf_path": create_pdf(comic)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
