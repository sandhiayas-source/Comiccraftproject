import requests

BASE = "http://127.0.0.1:8000"

r = requests.get(f"{BASE}/health", timeout=10)
r.raise_for_status()

payload = {
    "title": "Milo the Brave Little Fox",
    "character": "Milo (Fox)",
    "setting": "Village & Enchanted Forest",
    "tone": "Warm and funny",
    "art_style": "Colorful Comic Book",
    "pages": 5,
    "use_ai": False
}

r = requests.post(f"{BASE}/api/comic/generate", json=payload, timeout=60)
r.raise_for_status()
data = r.json()

assert len(data["pages"]) == 5
assert data["moral"]
print("ComicCraft smoke test passed.")
