from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from app.schemas import ComicResponse
from app.utils.paths import PDF_DIR

def _wrap(text, width=85):
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + len(word) + 1 <= width:
            current = (current + " " + word).strip()
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def create_pdf(comic: ComicResponse) -> str:
    path = PDF_DIR / "comiccraft_comic.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setTitle(comic.title)

    for page in comic.pages:
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width / 2, height - 55, comic.title)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(45, height - 95, f"Page {page.page_number}: {page.title}")

        y = height - 125
        if page.image_url:
            try:
                c.drawImage(
                    ImageReader(page.image_url), 45, y - 320,
                    width=width - 90, height=300,
                    preserveAspectRatio=True, anchor="c"
                )
                y -= 340
            except Exception:
                pass

        c.setFont("Helvetica", 12)
        for line in _wrap(page.description):
            c.drawString(45, y, line)
            y -= 17

        y -= 10
        c.setFont("Helvetica-Oblique", 12)
        for line in _wrap(f'Dialogue: "{page.dialogue}"'):
            c.drawString(45, y, line)
            y -= 17
        c.showPage()

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 80, "Moral of the Story")
    c.setFont("Helvetica", 14)
    y = height - 125
    for line in _wrap(comic.moral, 70):
        c.drawCentredString(width / 2, y, line)
        y -= 22
    c.setFont("Helvetica-Oblique", 16)
    c.drawCentredString(width / 2, y - 25, "Dream - Create - Be Kind")
    c.save()
    return str(path)
