from log_utils import debug_log, output_log
import os
import requests
from markdownify import markdownify as md
from getpass import getpass
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()


CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")
SPACE_KEYS = os.getenv("CONFLUENCE_SPACE_KEYS", "VYAGUTA,LEAP").split(",")
SPACE_KEYS = [k.strip() for k in SPACE_KEYS if k.strip()]
OUTPUT_DIR = "docs-confluence"

if not CONFLUENCE_BASE_URL or not EMAIL or not API_TOKEN:
    output_log(
        "Please add CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN to your .env file."
    )
    exit(1)


def get_space_key():
    if SPACE_KEY:
        return SPACE_KEY
    space_key = input("Enter your Confluence space key (e.g., HR, DEV, ENG): ").strip()
    if not space_key:
        output_log("Space key is required.")
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

    results = data.get("page", data.get("pages", {})).get("results", [])
    return [(p["id"], p["title"]) for p in results]


def fetch_and_save_page(page_id, title, output_dir):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    auth = (EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}
    resp = requests.get(url, auth=auth, headers=headers)
    resp.raise_for_status()
    html = resp.json()["body"]["storage"]["value"]
    md_content = md(html)
    filename = f"{title.replace('/', '_').replace(' ', '_')}.md"
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(md_content)
    output_log(f"Saved: {filename} in {output_dir}")


def get_all_pages(space_key):
    """
    Recursively fetch all pages and subpages in the given Confluence space.
    Returns a list of (page_id, title) tuples for all pages.
    """
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"
    params = {"spaceKey": space_key, "limit": 100, "expand": "ancestors,children.page"}
    auth = (EMAIL, API_TOKEN)
    headers = {"Accept": "application/json"}
    all_pages = []
    seen_ids = set()
    MAX_DEPTH = 20

    def fetch_page_and_children(page, depth=0):
        if depth > MAX_DEPTH:
            output_log(
                f"Maximum depth of {MAX_DEPTH} reached for page {page['id']} ({page['title']}). Skipping further recursion."
            )
            return
        page_id = page["id"]
        title = page["title"]
        if page_id in seen_ids:
            return
        seen_ids.add(page_id)  # Mark the page as seen before processing
        all_pages.append((page_id, title))
        # Recursively fetch children
        children = page.get("children", {}).get("page", {}).get("results", [])
        for child in children:
            fetch_page_and_children(child, depth + 1)

    # Initial fetch: get all root pages
    while url:
        resp = requests.get(url, auth=auth, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        for page in results:
            fetch_page_and_children(page)
        # Pagination
        url = data.get("_links", {}).get("next")
        if url:
            url = CONFLUENCE_BASE_URL + url
        params = None
    return all_pages


def main():
    for space_key in SPACE_KEYS:
        output_dir = os.path.join("docs-confluence", space_key.lower())
        output_log(f"Fetching ALL pages (including subpages) from space: {space_key}")
        pages = get_all_pages(space_key)
        if not pages:
            output_log(
                f"No pages found in space {space_key} or you may not have access."
            )
            continue
        for page_id, title in pages:
            fetch_and_save_page(page_id, title, output_dir)
        output_log(
            f"All pages and subpages fetched and saved as markdown in the {output_dir}/ folder."
        )


if __name__ == "__main__":
    main()
