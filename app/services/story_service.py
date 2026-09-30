import json
import os
from openai import OpenAI
from app.schemas import ComicRequest, ComicResponse, ComicPage

REFERENCE_PAGES = [
    ("A Little Dream", "Milo the fox decides today is the day he will become a hero.", "I will help someone!"),
    ("A Kind Encounter", "Milo meets a small rabbit who is worried about a lost way home.", "Don't worry. I'll help you!"),
    ("The Big Crossing", "A rushing stream blocks the path, so Milo searches for a safe route across.", "Together, we can do it!"),
    ("A Brave Choice", "A storm arrives, and Milo uses quick thinking to guide everyone to shelter.", "Follow me! This way!"),
    ("A New Hero", "The friends reach safety. Milo learns that kindness and trying your best are what matter.", "I don't need to be perfect to help."),
]
MORAL = "You do not need to be perfect to make a difference. Be kind, be brave, and keep trying."

def _fallback(request: ComicRequest) -> ComicResponse:
    selected = REFERENCE_PAGES[:request.pages]
    while len(selected) < request.pages:
        n = len(selected) + 1
        selected.append((
            f"A New Adventure {n - 5}",
            f"{request.character} continues exploring the {request.setting} and helps another friend.",
            "We can solve this together!"
        ))
    return ComicResponse(
        title=request.title,
        tagline="Big dreams. Kind choices. One small hero.",
        pages=[
            ComicPage(page_number=i + 1, title=t, description=d, dialogue=q)
            for i, (t, d, q) in enumerate(selected)
        ],
        moral=MORAL,
    )

def generate_story(request: ComicRequest) -> ComicResponse:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not request.use_ai or not api_key:
        return _fallback(request)

    client = OpenAI(api_key=api_key)
    prompt = f"""
Create a positive, age-appropriate children's comic.

Title: {request.title}
Main character: {request.character}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}
Number of pages: {request.pages}

Return ONLY valid JSON with:
{{
  "title": "...",
  "tagline": "...",
  "pages": [
    {{"page_number": 1, "title": "...", "description": "...", "dialogue": "..."}}
  ],
  "moral": "..."
}}
"""
    result = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.8,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You create concise children's comic stories."},
            {"role": "user", "content": prompt},
        ],
    )
    return ComicResponse.model_validate(json.loads(result.choices[0].message.content))
