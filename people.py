# TODO Case for multiple people with the same name
# TODO Data not trained for handling more detailed people queries

import os
import re
import glob
import markdown
from config import API_PEOPLE_URL, VYAGUTA_BASE_URL
from auth import refresh_access_token, app_startup


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


def load_people_from_markdown(directory="docs-api/people"):
    people = []
    for md_file in glob.glob(os.path.join(directory, "*.md")):
        with open(md_file, encoding="utf-8") as f:
            content = f.read()
        # Simple parsing: extract fields from markdown bullet points
        person = {}
        lines = content.splitlines()
        # First line is the name header
        if lines and lines[0].startswith("# "):
            person["name"] = lines[0][2:].replace("_", " ").strip()
        for line in lines:
            if line.startswith("- "):
                parts = line[2:].split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(" ", "_")
                    value = parts[1].strip()
                    person[key] = value
        people.append(person)
    return people


# --- Fetch all people (from markdown) ---
def fetch_people_data():
    return load_people_from_markdown()


# --- Fetch detailed info for a person by ID (from markdown) ---
def fetch_person_details_by_id(person_id):
    people = load_people_from_markdown()
    for person in people:
        if person.get("employee_id") == str(person_id) or person.get("id") == str(
            person_id
        ):
            return person
    return None


def get_people_matches(name_or_email, people_data):
    name_or_email = name_or_email.strip().lower()
    matches = []
    # Match by email (exact)
    for person in people_data:
        if person.get("email", "").lower() == name_or_email:
            matches.append(person)
    # Match by name (partial, case-insensitive)
    for person in people_data:
        name = person.get("name", "").lower()
        if name_or_email in name and person not in matches:
            matches.append(person)
        # Also match first/middle/last if available
        for key in ["first_name", "middle_name", "last_name"]:
            if (
                key in person
                and name_or_email in person[key].lower()
                and person not in matches
            ):
                matches.append(person)
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


# --- Check if the question is about the total number of people ---
def is_total_people_query(question):
    """
    Returns True if the question is asking for the total number of people/employees at Leapfrog.
    """
    q = question.lower()
    patterns = [
        r"how many people",
        r"total number of people",
        r"number of employees",
        r"how many employees",
        r"total employees",
        r"total leapfroggers",
        r"how many leapfroggers",
        r"total participants",
        r"number of participants",
    ]
    return any(re.search(pat, q) for pat in patterns)


# --- Extract field count query ---
def extract_field_count_query(question):
    """
    Returns (field, value) if the question is asking for the count of people by a field (designation, department, gender, etc.).
    E.g. "How many Associate Software Engineer are there?", "How many people in Engineering?", "How many males?"
    """
    q = question.lower()
    # Designation
    m = re.search(r"how many ([\w\s\(\)\-]+) are there", q)
    if m:
        return ("designation", m.group(1).strip())
    # Department
    m = re.search(r"how many people in ([\w\s\(\)\-]+)", q)
    if m:
        return ("department", m.group(1).strip())
    # Gender
    m = re.search(r"how many (male|female|males|females|men|women)", q)
    if m:
        gender = m.group(1)
        if gender in ["male", "males", "men"]:
            return ("gender", "male")
        else:
            return ("gender", "female")
    return (None, None)


# --- Extract field list query ---
def extract_field_list_query(question):
    """
    Returns field if the question is asking to list all values of a field (departments, designations, etc.)
    E.g. "List all departments", "Show all designations"
    """
    q = question.lower()
    if "list all departments" in q or "show all departments" in q:
        return "department"
    if "list all designations" in q or "show all designations" in q:
        return "designation"
    return None


# --- Main function: answer people-related questions ---
def get_person_info_from_question(question, people_data=None):
    people_data = fetch_people_data()
    lower_q = question.strip().lower()
    # --- Count queries by field ---
    field, value = extract_field_count_query(question)
    if field and value:
        count = 0
        names = []
        for person in people_data:
            if field == "designation":
                designation = person.get("designation", "").lower()
                if normalize_designation(value) == normalize_designation(designation):
                    count += 1
                    names.append(person.get("name", "N/A"))
            elif field == "department":
                department = person.get("department", "").lower()
                if normalize_department(value) == normalize_department(department):
                    count += 1
                    names.append(person.get("name", "N/A"))
            elif field == "gender":
                gender = person.get("gender", "").lower()
                if normalize_gender(value) == normalize_gender(gender):
                    count += 1
                    names.append(person.get("name", "N/A"))
        if count == 0:
            return f"There are 0 {value.title()}s at Leapfrog."
        if count <= 10:
            return (
                f"There are {count} {value.title()}s at Leapfrog: {', '.join(names)}."
            )
        return f"There are {count} {value.title()}s at Leapfrog."

    # --- List queries by field ---
    list_field = extract_field_list_query(question)
    if list_field:
        values = set()
        for person in people_data:
            if list_field == "designation":
                values.add(normalize_designation(person.get("designation", "N/A")))
            elif list_field == "department":
                values.add(normalize_department(person.get("department", "N/A")))
        return f"All {list_field}s at Leapfrog: {', '.join(sorted(values))}"

    if is_total_people_query(question):
        total = len(people_data)
        return f"There are {total} people at Leapfrog."
    if not is_people_query(question):
        return None
    print("[DEBUG] get_person_info_from_question called with question:", question)
    # 1. API endpoint explanation
    api_explanation = explain_api_endpoint(question)
    if api_explanation:
        print("[DEBUG] API explanation triggered.")
        return api_explanation

    # --- Improved name matching ---
    name_query = lower_q
    matches = get_people_matches(name_query, people_data)
    if matches:
        # If multiple matches, show a list for disambiguation
        if len(matches) > 1:
            lines = [
                f"Found {len(matches)} people matching your query. Please specify which one you mean, or see details below:"
            ]
            for idx, person_info in enumerate(matches, 1):
                lines.append(f"[{idx}]\n" + format_full_person_info(person_info) + "\n")
            return "\n".join(lines)
        # Otherwise, show rich info for the single match
        person_info = matches[0]
        return format_full_person_info(person_info)
    return None


# --- Helper to format all available fields for a person ---
def format_full_person_info(person_info):
    """
    Formats all available fields of a person into a creative, multi-line, rich output.
    """
    lines = []
    name = person_info.get("name", person_info.get("fullName", "N/A"))
    emp_id = person_info.get("employee_id", person_info.get("id", "N/A"))
    designation = person_info.get("designation", "N/A")
    department = person_info.get("department", "N/A")
    email = person_info.get("email", "N/A")
    mobile = person_info.get("mobile", person_info.get("mobile_phone", "N/A"))
    gender = person_info.get("gender", "N/A")
    birthday = person_info.get("birthday", "N/A")
    join_date = person_info.get("join_date", "N/A")
    address = person_info.get("address", "N/A")
    blood_group = person_info.get("blood_group", "N/A")
    personal_email = person_info.get("personal_email", "N/A")
    emergency_phone = person_info.get("emergency_phone", "N/A")
    emergency_contact_relationship = person_info.get(
        "emergency_contact_relationship", "N/A"
    )
    github_id = person_info.get("githubid", person_info.get("github_id", "N/A"))
    avatar_url = person_info.get("avatar_url", "N/A")
    timezone = person_info.get("timezone", "N/A")
    past_experience = person_info.get("past_experience", "N/A")
    emp_status = person_info.get("emp_status", "N/A")
    working_shift = person_info.get("working_shift", "N/A")
    maritial_status = person_info.get("maritial_status", "N/A")
    lines.append(f"Name: {name}")
    lines.append(f"Employee ID: {emp_id}")
    lines.append(f"Designation: {designation}")
    lines.append(f"Department: {department}")
    lines.append(f"Email: {email}")
    lines.append(f"Mobile: {mobile}")
    lines.append(f"Gender: {gender}")
    lines.append(f"Birthday: {birthday}")
    lines.append(f"Join Date: {join_date}")
    lines.append(f"Address: {address}")
    lines.append(f"Blood Group: {blood_group}")
    lines.append(f"Personal Email: {personal_email}")
    lines.append(f"Emergency Phone: {emergency_phone}")
    lines.append(f"Emergency Contact Relationship: {emergency_contact_relationship}")
    lines.append(f"Github ID: {github_id}")
    lines.append(f"Avatar URL: {avatar_url}")
    lines.append(f"Timezone: {timezone}")
    lines.append(f"Past Experience: {past_experience}")
    lines.append(f"Employment Status: {emp_status}")
    lines.append(f"Working Shift: {working_shift}")
    lines.append(f"Maritial Status: {maritial_status}")
    # Skills
    skills = person_info.get("skills", None)
    skill_names = []
    if skills and skills != "N/A":
        if isinstance(skills, str):
            try:
                import ast

                parsed_skills = ast.literal_eval(skills)
                if isinstance(parsed_skills, list):
                    skill_names = [
                        s.get("name", str(s))
                        for s in parsed_skills
                        if isinstance(s, dict)
                    ]
                    if not skill_names:
                        skill_names = [str(s) for s in parsed_skills]
                else:
                    skill_names = [skills]
            except Exception:
                skill_names = [skills]
        elif isinstance(skills, list):
            skill_names = [s.get("name", str(s)) for s in skills if isinstance(s, dict)]
            if not skill_names:
                skill_names = [str(s) for s in skills]
        if skill_names:
            lines.append(f"Skills: {', '.join(skill_names)}")

    # Nested fields
    def format_person_field(field):
        if isinstance(field, dict):
            fn = field.get("firstName", "")
            mn = field.get("middleName", "")
            ln = field.get("lastName", "")
            email = field.get("email", "")
            empid = field.get("empId", field.get("id", ""))
            return f"{fn} {mn} {ln} (Email: {email}, ID: {empid})".replace(
                "  ", " "
            ).strip()
        return str(field)

    supervisor = person_info.get("supervisor", None)
    if supervisor and supervisor != "N/A":
        lines.append(f"Supervisor: {format_person_field(supervisor)}")
    coach = person_info.get("coach", None)
    if coach and coach != "N/A":
        lines.append(f"Coach: {format_person_field(coach)}")
    team_manager = person_info.get("teammanager", person_info.get("team_manager", None))
    if team_manager and team_manager != "N/A":
        lines.append(f"Team Manager: {format_person_field(team_manager)}")
    leave_issuer = person_info.get("leave_issuer", None)
    if leave_issuer and leave_issuer != "N/A":
        lines.append(f"Leave Issuer: {format_person_field(leave_issuer)}")
    # Add any other available fields not already shown
    shown_keys = set(
        [
            "name",
            "employee_id",
            "id",
            "designation",
            "department",
            "email",
            "mobile",
            "mobile_phone",
            "gender",
            "join_date",
            "birthday",
            "address",
            "blood_group",
            "avatar_url",
            "personal_email",
            "emergency_phone",
            "emergency_contact_relationship",
            "githubid",
            "skills",
            "supervisor",
            "coach",
            "teammanager",
            "team_manager",
            "leave_issuer",
            "timezone",
            "past_experience",
            "emp_status",
            "working_shift",
            "maritial_status",
        ]
    )
    for key, value in person_info.items():
        if key not in shown_keys and value and value != "N/A":
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def normalize_designation(designation):
    """
    Normalize designation for matching (handles abbreviations, plural, etc.)
    """
    d = designation.lower().strip()
    if d in ["ase", "associate software engineer", "associate software engineers"]:
        return "associate software engineer"
    # Add more normalization rules as needed
    return d


def normalize_department(department):
    d = department.lower().strip()
    # Add more normalization rules as needed
    return d


def normalize_gender(gender):
    g = gender.lower().strip()
    if g in ["male", "males", "men"]:
        return "male"
    if g in ["female", "females", "women"]:
        return "female"
    return g


def generate_people_docs(people_data):
    """
    Converts people data (from markdown) into text chunks for RAG ingestion.
    Each person becomes a short summary string.
    """
    docs = []
    for person in people_data:
        name = person.get("name", "N/A")
        designation = person.get("designation", person.get("designation", "N/A"))
        department = person.get("department", person.get("department", "N/A"))
        email = person.get("email", "N/A")
        mobile = person.get("mobile", person.get("mobile_phone", "N/A"))
        summary = f"{name}: {designation}, {department}, {email}, {mobile}"
        docs.append(summary)
    return docs
