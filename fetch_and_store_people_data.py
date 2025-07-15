import os
import sys
from dotenv import load_dotenv
import requests
from config import API_PEOPLE_URL
from auth import app_startup

# --- Load environment variables from .env file (like main.py) ---
load_dotenv()

# --- Check for VYAGUTA_REFRESH_TOKEN before authentication ---
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


def save_people_to_markdown(people, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for person in people:
        person_id = person.get("id")
        details = fetch_person_details_by_id(person_id) if person_id else person
        if not details:
            details = person
        emp_id = details.get("empId") or details.get("id")
        name = f"{details.get('firstName', '')} {details.get('middleName', '') or ''} {details.get('lastName', '')}".strip().replace(
            " ", "_"
        )
        filename = f"{emp_id}_{name}.md"
        path = os.path.join(out_dir, filename)
        designation = (
            details.get("designation", {}).get("name", "N/A")
            if isinstance(details.get("designation"), dict)
            else details.get("designation", "N/A")
        )
        department = (
            details.get("department", {}).get("name", "N/A")
            if isinstance(details.get("department"), dict)
            else details.get("department", "N/A")
        )
        email = details.get("email", "N/A")
        mobile = details.get("mobilePhone", "N/A")
        gender = details.get("gender", "N/A")
        birthday = details.get(
            "birthday", details.get("dateOfBirth", details.get("dateofBirth", "N/A"))
        )
        address = details.get(
            "permanentAddress",
            details.get(
                "address", details.get("location", details.get("country", "N/A"))
            ),
        )
        join_date = details.get(
            "joinDate", details.get("employeeSince", details.get("joiningDate", "N/A"))
        )
        blood_group = details.get("bloodGroup", "N/A")
        avatar_url = details.get("avatarUrl", "N/A")
        leave_issuer = details.get("leaveIssuer", "N/A")
        # Add all other available fields for completeness
        other_fields = ""
        for k, v in details.items():
            if k not in [
                "empId",
                "id",
                "firstName",
                "middleName",
                "lastName",
                "designation",
                "department",
                "email",
                "mobilePhone",
                "gender",
                "birthday",
                "dateOfBirth",
                "dateofBirth",
                "permanentAddress",
                "address",
                "location",
                "country",
                "joinDate",
                "employeeSince",
                "joiningDate",
                "bloodGroup",
                "avatarUrl",
                "leaveIssuer",
            ]:
                other_fields += f"- {k}: {v}\n"
        md = f"""# {name}

- Employee ID: {emp_id}
- Designation: {designation}
- Department: {department}
- Email: {email}
- Mobile: {mobile}
- Gender: {gender}
- Birthday: {birthday}
- Join Date: {join_date}
- Address: {address}
- Blood Group: {blood_group}
- Avatar URL: {avatar_url}
- Leave Issuer: {leave_issuer}
{other_fields}"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
    print(f"Saved {len(people)} markdown files to {out_dir}")


def main():
    app_startup()
    people = fetch_all_people()
    save_people_to_markdown(people, "docs-api/people/")


if __name__ == "__main__":
    main()
