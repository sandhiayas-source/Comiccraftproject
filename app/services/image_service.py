import base64
import os
from openai import OpenAI
from app.utils.paths import IMAGE_DIR

def _svg_fallback(title, description, dialogue, character, art_style, page_number):
    def safe(s):
        return (str(s).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
<rect width="1200" height="800" fill="#fff8e7"/>
<rect x="35" y="35" width="1130" height="730" rx="28" fill="white" stroke="#222" stroke-width="8"/>
<text x="600" y="100" text-anchor="middle" font-family="Arial" font-size="42" font-weight="bold">{safe(title)}</text>
<circle cx="600" cy="330" r="125" fill="#f28c28" stroke="#222" stroke-width="8"/>
<circle cx="555" cy="305" r="14" fill="#222"/><circle cx="645" cy="305" r="14" fill="#222"/>
<path d="M550 365 Q600 410 650 365" fill="none" stroke="#222" stroke-width="8"/>
<path d="M510 245 L535 155 L575 235 M690 235 L730 155 L750 260" fill="#f28c28" stroke="#222" stroke-width="8"/>
<text x="600" y="530" text-anchor="middle" font-family="Arial" font-size="28">{safe(character)} — {safe(art_style)}</text>
<text x="600" y="590" text-anchor="middle" font-family="Arial" font-size="25">{safe(description[:85])}</text>
<rect x="170" y="625" width="860" height="95" rx="22" fill="#f4f4f4" stroke="#222" stroke-width="5"/>
<text x="600" y="685" text-anchor="middle" font-family="Arial" font-size="27">“{safe(dialogue)}”</text>
<text x="1120" y="740" text-anchor="end" font-family="Arial" font-size="20">Page {page_number}</text>
</svg>"""
    path = IMAGE_DIR / f"page_{page_number}.svg"
    path.write_text(svg, encoding="utf-8")
    return str(path)

def generate_page_image(title, description, dialogue, character, art_style, page_number):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _svg_fallback(title, description, dialogue, character, art_style, page_number)

    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            f"Children's comic book panel, colorful and friendly. "
            f"Character: {character}. Art style: {art_style}. "
            f"Scene title: {title}. Scene: {description}. "
            "No readable text, no watermark, landscape composition."
        )
        result = client.images.generate(
            model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1"),
            prompt=prompt,
            size="1536x1024",
        )
        raw = base64.b64decode(result.data[0].b64_json)
        path = IMAGE_DIR / f"page_{page_number}.png"
        path.write_bytes(raw)
        return str(path)
    except Exception:
        return _svg_fallback(title, description, dialogue, character, art_style, page_number)
