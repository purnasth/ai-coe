# TODO: Integrate Confluence data fetching with the main RAG pipeline (automatic connection)

import os
import requests
from markdownify import markdownify as md
from getpass import getpass
from urllib.parse import quote
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
OUTPUT_DIR = "docs-confluence"

if not CONFLUENCE_BASE_URL or not EMAIL or not API_TOKEN:
    print(
        "Please add CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN to your .env file."
    )
    exit(1)


def get_space_key():
    if SPACE_KEY:
        return SPACE_KEY
    space_key = input("Enter your Confluence space key (e.g., HR, DEV, ENG): ").strip()
    if not space_key:
        print("Space key is required.")
        exit(1)
    return space_key


def get_page_ids(space_key):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/space/{quote(space_key)}/content"
    params = {"limit": 100, "expand": "body.storage"}
    auth = (EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}
    resp = requests.get(url, auth=auth, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    # Some Confluence instances use 'page', others 'pages'
    results = data.get("page", data.get("pages", {})).get("results", [])
    return [(p["id"], p["title"]) for p in results]


def fetch_and_save_page(page_id, title):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    auth = (EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}
    resp = requests.get(url, auth=auth, headers=headers)
    resp.raise_for_status()
    html = resp.json()["body"]["storage"]["value"]
    md_content = md(html)
    filename = f"{title.replace('/', '_').replace(' ', '_')}.md"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved: {filename}")


def main():
    space_key = get_space_key()
    print(f"Fetching pages from space: {space_key}")
    pages = get_page_ids(space_key)
    if not pages:
        print("No pages found in this space or you may not have access.")
        return
    for page_id, title in pages:
        fetch_and_save_page(page_id, title)
    print("All pages fetched and saved as markdown in the docs/ folder.")


if __name__ == "__main__":
    main()
