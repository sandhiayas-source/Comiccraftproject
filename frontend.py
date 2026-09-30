import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(page_title="ComicCraft AI", page_icon="🦊", layout="wide")
st.title("🦊 ComicCraft AI")
st.caption("AI Comic Story Creator — Dream • Create • Be Kind")

with st.sidebar:
    st.header("Story Settings")
    title = st.text_input("Title", "Milo the Brave Little Fox")
    character = st.text_input("Main character", "Milo (Fox)")
    setting = st.text_input("Setting", "Village & Enchanted Forest")
    tone = st.selectbox("Tone", ["Warm and funny", "Adventure", "Funny", "Emotional", "Educational"])
    art_style = st.selectbox("Art style", ["Colorful Comic Book", "Cartoon", "Watercolor", "Children's Book"])
    pages = st.slider("Story pages", 3, 8, 5)
    use_ai = st.checkbox("Use external AI when API key is configured", True)

if "comic" not in st.session_state:
    st.session_state.comic = None

if st.button("✨ Generate Comic", type="primary", use_container_width=True):
    payload = {
        "title": title, "character": character, "setting": setting,
        "tone": tone, "art_style": art_style, "pages": pages, "use_ai": use_ai
    }
    try:
        with st.spinner("Creating your comic..."):
            r = requests.post(f"{BACKEND_URL}/api/comic/generate", json=payload, timeout=180)
            r.raise_for_status()
            st.session_state.comic = r.json()
        st.success("Comic created successfully!")
    except Exception as exc:
        st.error(f"Could not generate the comic: {exc}")
        st.info("Start the FastAPI backend on port 8000 first.")

comic = st.session_state.comic
if comic:
    st.subheader(comic["title"])
    st.write(comic["tagline"])

    for page in comic["pages"]:
        st.markdown(f"### Page {page['page_number']} — {page['title']}")
        left, right = st.columns([1.4, 1])
        with left:
            image_path = page.get("image_url")
            if image_path and os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
        with right:
            st.write(page["description"])
            st.markdown(f"**Dialogue:** “{page['dialogue']}”")

    st.subheader("🌱 Moral of the Story")
    st.info(comic["moral"])

    if st.button("📕 Create PDF"):
        try:
            with st.spinner("Building PDF..."):
                r = requests.post(f"{BACKEND_URL}/api/comic/pdf", json=comic, timeout=120)
                r.raise_for_status()
                pdf_path = r.json()["pdf_path"]
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Comic PDF", f,
                        file_name="comiccraft_comic.pdf", mime="application/pdf"
                    )
            else:
                st.error("PDF path was returned but the file was not found.")
        except Exception as exc:
            st.error(f"PDF generation failed: {exc}")
