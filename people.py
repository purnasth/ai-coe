
# TODO Case for multiple people with the same name
# TODO Data not trained for handling more detailed people queries

import requests
import re


# --- API endpoint explanations ---
def explain_api_endpoint(question):
    api_patterns = [r"vyaguta\\.lftechnology\\.com/api/core/users", r"/api/core/users"]
    for pat in api_patterns:
        if re.search(pat, question):
            return (
                "The API endpoint https://vyaguta.lftechnology.com/api/core/users provides a list of Leapfrog employees (Leapfroggers) with details such as first name, last name, email, mobile phone, department, and designation. "
                "It is used to fetch people data for search, lookup, and onboarding features in Vyaguta and related tools. "
                "The endpoint supports pagination and returns structured user information for internal use."
            )
    return None


# --- Helper for stemming and synonyms ---
def normalize_word(word):
    for suf in ["ers", "ies", "ers", "ors", "ists", "ings", "ments", "ships", "s"]:
        if word.endswith(suf) and len(word) > len(suf) + 2:
            word = word[: -len(suf)]
            break
    synonyms = {
        "developer": "develop",
        "development": "develop",
        "dev": "develop",
        "engineer": "engineer",
        "engineering": "engineer",
        "designer": "design",
        "design": "design",
        "qa": "qa",
        "quality": "qa",
        "product": "product",
        "manager": "manager",
        "lead": "lead",
        "analyst": "analyst",
        "associate": "associate",
        "intern": "intern",
        "director": "director",
        "secops": "secops",
        "sysops": "sysops",
        "frontend": "front",
        "front-end": "front",
        "backend": "back",
        "back-end": "back",
        "devops": "devop",
        "ai": "ai",
        "data": "data",
    }
    w = word.lower()
    return synonyms.get(w, w)


# --- Fetch all people (basic info) ---
def fetch_people_data():
    import os

    base_url = (
        "https://vyaguta.lftechnology.com/api/core/users?order=ASC&sortBy=firstName&fields="
        "avatarUrl%2CmobilePhone%2Cdepartment%2Cdesignation%2CleaveIssuer"
    )
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


# --- Generate RAG-friendly people docs ---
def generate_people_docs(people_data):
    """
    Converts people data into text chunks for RAG ingestion.
    Each person becomes a short summary string.
    """
    docs = []
    for person in people_data:
        name = f"{person.get('firstName', '')} {person.get('middleName', '') or ''} {person.get('lastName', '')}".strip()
        designation = person.get("designation", {}).get("name", "N/A")
        department = person.get("department", {}).get("name", "N/A")
        email = person.get("email", "N/A")
        mobile = person.get("mobilePhone", "N/A")
        summary = f"{name}: {designation}, {department}, {email}, {mobile}"
        docs.append(summary)
    return docs


# --- Fetch detailed info for a person by ID ---
def fetch_person_details_by_id(person_id):
    url = f"https://vyaguta.lftechnology.com/api/core/users/{person_id}"
    import os

    token = os.getenv("VYAGUTA_ACCESS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    print("[DEBUG] Fetching detailed user info:")
    print("[DEBUG] URL:", url)
    print("[DEBUG] Token:", token)
    print("[DEBUG] Headers:", headers)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print("[DEBUG] Status Code:", response.status_code)
        print("[DEBUG] Response Text:", response.text)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Warning: Could not fetch details for person ID {person_id}. {e}")
        return None


# --- Fuzzy/partial matching for people ---
def get_people_matches(name_or_email, people_data):
    # Only allow exact email match; all other queries should fall back to RAG
    name_or_email = name_or_email.strip().lower()
    matches = [
        person
        for person in people_data
        if person.get("email", "").lower() == name_or_email
    ]
    return matches


# --- Check if the question is about a person ---
def is_people_query(question):
    """
    Returns True if the question is likely about a person (name, people info, or people-related keywords).
    """
    q = question.lower()
    # Common people-related keywords
    keywords = [
        "who is",
        "whose",
        "contact",
        "email of",
        "mobile of",
        "phone of",
        "birthday of",
        "born",
        "gender of",
        "address of",
        "where does",
        "when was",
        "joining date of",
        "supervisor of",
        "manager of",
        "coach of",
        "designation of",
        "department of",
        "team of",
        "leave issuer of",
        "what is the gender",
        "what is the birthday",
        "what is the address",
        "what is the email",
        "what is the phone",
        "what is the mobile",
        "what is the designation",
        "what is the department",
        "what is the team",
        "what is the supervisor",
        "what is the manager",
        "what is the coach",
        "what is the leave issuer",
        "show info for",
        "show details for",
        "tell me about",
        "profile of",
        "employee ",
        "person ",
        "people ",
        "leapfrogger",
        "leapfroggers",
    ]
    # If any keyword is present, it's a people query
    if any(kw in q for kw in keywords):
        return True
    # If the question matches a pattern like "What is the gender of <Name>" or "When was <Name> born"
    if re.search(
        r"(gender|birthday|address|email|phone|mobile|designation|department|team|supervisor|manager|coach|leave issuer|born|joining date|profile|info|details) of [a-zA-Z]",
        q,
    ):
        return True
    # If the question starts with "Who is" or "Tell me about"
    if re.match(
        r"^(who is|tell me about|profile of|show info for|show details for)", q
    ):
        return True
    return False


# --- Main function: answer people-related questions ---
def get_person_info_from_question(question, people_data):
    if not is_people_query(question):
        return None
    print("[DEBUG] get_person_info_from_question called with question:", question)
    # 1. API endpoint explanation
    api_explanation = explain_api_endpoint(question)
    if api_explanation:
        print("[DEBUG] API explanation triggered.")
        return api_explanation

    lower_q = question.strip().lower()
    # Only handle exact email match deterministically; all other queries fall back to RAG
    # Always try to match by name or email for deterministic people info
    # Try email match first
    email_match = re.search(r"[\w.]+@[\w.]+", lower_q)
    matches = []
    if email_match:
        search_term = email_match.group(0)
        matches = [p for p in people_data if p.get("email", "").lower() == search_term]
    else:
        # Try to match by first name, last name, or full name (case-insensitive, exact)
        words = set(lower_q.split())
        for person in people_data:
            first_name = person.get("firstName", "").strip().lower()
            last_name = person.get("lastName", "").strip().lower()
            middle_name = (person.get("middleName", "") or "").strip().lower()
            full_name = f"{first_name} {middle_name} {last_name}".replace(
                "  ", " "
            ).strip()
            # Match if any word matches first, middle, or last name, or if the question contains the full name
            if (
                first_name in words
                or last_name in words
                or (middle_name and middle_name in words)
                or full_name in lower_q
                or f"{first_name} {last_name}" in lower_q
            ):
                matches.append(person)
    if matches:
        # If multiple matches, show a list for disambiguation
        if len(matches) > 1:
            lines = [
                "Multiple people found matching your query. Please specify which one you mean:"
            ]
            for idx, person_info in enumerate(matches, 1):
                name = f"{person_info.get('firstName', '').title()} {person_info.get('middleName', '') or ''}{person_info.get('lastName', '').title()}".strip()
                email = person_info.get("email", "N/A")
                department = (
                    person_info.get("department", {}).get("name", "N/A")
                    if isinstance(person_info.get("department"), dict)
                    else person_info.get("department", "N/A")
                )
                designation = (
                    person_info.get("designation", {}).get("name", "N/A")
                    if isinstance(person_info.get("designation"), dict)
                    else person_info.get("designation", "N/A")
                )
                more_info_url = f"https://vyaguta.lftechnology.com/leapfroggers/{person_info.get('id', '')}"
                lines.append(
                    f"[{idx}] {name} | {designation}, {department} | Email: {email} | More info: {more_info_url}"
                )
            return "\n".join(lines)

        # Otherwise, show detailed info for the single match
        person_info = matches[0]
        person_id = person_info.get("id")
        details = fetch_person_details_by_id(person_id) if person_id else None
        data = details.get("data", details) if details else person_info

        name = f"{data.get('firstName', '').title()} {data.get('middleName', '') or ''}{data.get('lastName', '').title()}".strip()
        email = data.get("email", "N/A")
        mobile = data.get("mobilePhone", "N/A")
        department = (
            data.get("department", {}).get("name", "N/A")
            if isinstance(data.get("department"), dict)
            else data.get("department", "N/A")
        )
        designation = (
            data.get("designation", {}).get("name", "N/A")
            if isinstance(data.get("designation"), dict)
            else data.get("designation", "N/A")
        )
        emp_id = data.get("empId", "N/A")
        gender = data.get("gender", "N/A")
        join_date = (
            data.get("joinDate")
            or data.get("employeeSince")
            or data.get("joiningDate")
            or "N/A"
        )
        birthday = (
            data.get("birthday")
            or data.get("dateOfBirth")
            or data.get("dateofBirth")
            or "N/A"
        )
        address = (
            data.get("permanentAddress")
            or data.get("address")
            or data.get("location")
            or data.get("country")
            or "N/A"
        )
        blood_group = data.get("bloodGroup", "N/A")
        more_info_url = (
            f"https://vyaguta.lftechnology.com/leapfroggers/{data.get('id', '')}"
        )

        answer_lines = [
            f"Name: {name}",
            f"Employee ID: {emp_id}",
            f"Designation: {designation}",
            f"Department: {department}",
            f"Email: {email}",
            f"Mobile: {mobile}",
            f"Gender: {gender}",
            f"Birthday: {birthday}",
            f"Join Date: {join_date}",
            f"Address: {address}",
            f"Blood Group: {blood_group}",
            f"For more info, please visit: {more_info_url}",
        ]
        # If the user asked for a specific field, return only that
        if any(
            k in lower_q for k in ["birthday", "birth date", "date of birth", "born"]
        ):
            return f"{name}'s birthday is {birthday}."
        if any(k in lower_q for k in ["gender"]):
            return f"{name}'s gender is {gender}."
        if any(k in lower_q for k in ["address", "location", "country"]):
            return f"{name}'s address is {address}."
        if any(k in lower_q for k in ["mobile", "phone"]):
            return f"{name}'s mobile number is {mobile}."
        if any(k in lower_q for k in ["email"]):
            return f"{name}'s email is {email}."
        if any(k in lower_q for k in ["department"]):
            return f"{name} works in the {department} department."
        if any(k in lower_q for k in ["designation"]):
            return f"{name}'s designation is {designation}."
        if any(k in lower_q for k in ["blood group"]):
            return f"{name}'s blood group is {blood_group}."
        if any(k in lower_q for k in ["join date", "joining date", "employee since"]):
            return f"{name} joined on {join_date}."
        return "\n".join(answer_lines)
    return None
