import os
import sys
from dotenv import load_dotenv
import requests
from config import API_PEOPLE_URL
from auth import app_startup

load_dotenv()

if not os.getenv("VYAGUTA_REFRESH_TOKEN"):
    print(
        "Error: VYAGUTA_REFRESH_TOKEN not set in environment. Please set it in your .env file or export it before running."
    )
    sys.exit(1)


def fetch_all_people():
    base_url = f"{API_PEOPLE_URL}?order=ASC&sortBy=firstName&fields=avatarUrl%2CmobilePhone%2Cdepartment%2Cdesignation%2CleaveIssuer"
    token = os.getenv("VYAGUTA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    all_people = []
    page = 1
    while True:
        url = f"{base_url}&page={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            people = data.get("data", [])
            if not people:
                break
            all_people.extend(people)
            meta = data.get("meta", {})
            total_pages = meta.get("totalPages")
            if total_pages and page >= total_pages:
                break
            page += 1
        except Exception as e:
            print(f"Warning: Could not fetch people data from API (page {page}). {e}")
            break
    return all_people


def fetch_person_details_by_id(person_id):
    from config import VYAGUTA_BASE_URL

    token = os.getenv("VYAGUTA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    url = f"{VYAGUTA_BASE_URL}/api/core/users/{person_id}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("data", {})
    except Exception as e:
        print(f"Warning: Could not fetch details for person ID {person_id}. {e}")
        return None


def save_people_to_markdown(people, out_dir, consolidated_file="people.md"):
    """
    Saves all people data as individual markdown files and a consolidated markdown file for RAG.
    Each person is serialized with all available fields in a standard format for LLM retrieval.
    """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    consolidated_md = ""
    for person in people:
        name_parts = [
            person.get("firstName", ""),
            person.get("middleName", ""),
            person.get("lastName", ""),
        ]
        name = " ".join([n for n in name_parts if n]).strip()
        safe_name = name.replace(" ", "_")
        emp_id = person.get("empId") or person.get("id")
        filename = f"{emp_id}_{safe_name}.md"
        path = os.path.join(out_dir, filename)

        md = f"# {name}\n\n"
        for k, v in person.items():
            if v not in (None, "None", "Not", "false", "N/A", "", []):
                md += f"- {k}: {v}\n"
        md += "\n---\n"
        consolidated_md += md

        with open(path, "w", encoding="utf-8") as f:
            f.write(md)

    with open(os.path.join(out_dir, consolidated_file), "w", encoding="utf-8") as f:
        f.write(consolidated_md)
    print(f"Saved {len(people)} markdown files and consolidated people.md to {out_dir}")


def main():
    app_startup()
    people = fetch_all_people()
    save_people_to_markdown(people, "docs-api/people/")


if __name__ == "__main__":
    main()
