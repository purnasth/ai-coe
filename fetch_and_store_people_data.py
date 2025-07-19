import os
import sys
import time
from dotenv import load_dotenv
import requests
from config import API_PEOPLE_URL
from auth import app_startup


# --- Debug logging ---
def debug_log(msg):
    env = os.getenv("ENV", "local").lower()
    if env in ("test", "testing"):  # Only show debug logs in test/testing
        print(f"[DEBUG {time.strftime('%H:%M:%S')}] {msg}")


# --- Output helper ---
def output_log(msg):
    print(f"[OUTPUT] {msg}")


load_dotenv()

if not os.getenv("VYAGUTA_REFRESH_TOKEN"):
    print(
        "Error: VYAGUTA_REFRESH_TOKEN not set in environment. Please set it in your .env file or export it before running."
    )
    sys.exit(1)


def fetch_all_people():
    debug_log("Fetching all people from API...")
    base_url = f"{API_PEOPLE_URL}?order=ASC&sortBy=firstName&fields=avatarUrl%2CmobilePhone%2Cdepartment%2Cdesignation%2CleaveIssuer"
    token = os.getenv("VYAGUTA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    all_people = []
    page = 1
    while True:
        url = f"{base_url}&page={page}"
        try:
            debug_log(f"Requesting page {page} from {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            people = data.get("data", [])
            if not people:
                debug_log(f"No more people found on page {page}.")
                break
            all_people.extend(people)
            meta = data.get("meta", {})
            total_pages = meta.get("totalPages")
            debug_log(
                f"Fetched {len(people)} people from page {page} (total so far: {len(all_people)})"
            )
            if total_pages and page >= total_pages:
                debug_log(f"Reached last page: {page} of {total_pages}")
                break
            page += 1
        except Exception as e:
            print(f"Warning: Could not fetch people data from API (page {page}). {e}")
            break
    debug_log(f"Total people fetched: {len(all_people)}")
    return all_people


def fetch_person_details_by_id(person_id):
    from config import VYAGUTA_BASE_URL

    token = os.getenv("VYAGUTA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"{VYAGUTA_BASE_URL}/api/core/users/{person_id}"
    try:
        debug_log(f"Fetching details for person ID {person_id} from {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        debug_log(f"Fetched details for person ID {person_id}")
        return response.json().get("data", {})
    except Exception as e:
        print(f"Warning: Could not fetch details for person ID {person_id}. {e}")
        return None


def save_people_to_markdown(people, out_dir, consolidated_file="people.md"):
    """
    Saves all people data as individual markdown files and a consolidated markdown file for RAG.
    Each person is serialized with all available fields from the API response in a standard format for LLM retrieval.
    """

    # SIMPLIFIED: Only generate a single consolidated people.md file (no per-person files)
    debug_log(
        f"Saving all people to a single markdown file: {os.path.join(out_dir, consolidated_file)}"
    )
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    consolidated_md = ""
    for idx, person in enumerate(people, 1):
        person_id = person.get("id")
        details = fetch_person_details_by_id(person_id) if person_id else person
        if not details:
            details = person
        name_parts = [
            details.get("firstName", ""),
            details.get("middleName", ""),
            details.get("lastName", ""),
        ]
        name = " ".join([n for n in name_parts if n]).strip()
        md = f"# {name}\n\n"
        for k, v in details.items():
            if v not in (None, "None", "Not", "false", "N/A", "", []):
                md += f"- {k}: {v}\n"
        md += "\n---\n"
        consolidated_md += md
        debug_log(f"[{idx}/{len(people)}] Added {name} to consolidated markdown")

    with open(os.path.join(out_dir, consolidated_file), "w", encoding="utf-8") as f:
        f.write(consolidated_md)
    output_log(f"Saved consolidated people.md with {len(people)} people to {out_dir}")


def main():
    debug_log("Starting app_startup() for authentication...")
    app_startup()
    debug_log("Authentication complete.")
    debug_log("Fetching people data...")
    people = fetch_all_people()
    debug_log("Saving people data to markdown...")
    save_people_to_markdown(people, "docs-api/people/")
    output_log("All people data fetched and saved.")


if __name__ == "__main__":
    main()
