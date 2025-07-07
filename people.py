def get_person_info_from_question(question, people_data):

    import re

    # --- API endpoint explanations ---
    api_patterns = [r"vyaguta\.lftechnology\.com/api/core/users", r"/api/core/users"]
    for pat in api_patterns:
        if re.search(pat, question):
            return (
                "The API endpoint https://vyaguta.lftechnology.com/api/core/users provides a list of Leapfrog employees (Leapfroggers) with details such as first name, last name, email, mobile phone, department, and designation. "
                "It is used to fetch people data for search, lookup, and onboarding features in Vyaguta and related tools. "
                "The endpoint supports pagination and returns structured user information for internal use."
            )

    # --- Helper for stemming and synonyms ---
    def normalize_word(word):
        # Simple stemming: remove common suffixes
        for suf in ["ers", "ies", "ers", "ors", "ists", "ings", "ments", "ships", "s"]:
            if word.endswith(suf) and len(word) > len(suf) + 2:
                word = word[: -len(suf)]
                break
        # Synonym/alias mapping
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

    """
    Parses a question, extracts a name or email, and returns formatted info if found.
    Args:
        question (str): The user's question.
        people_data (list): List of people dicts.
    Returns:
        str or None: Formatted info string if found, else None.
    """

    import re

    lower_q = question.strip().lower()
    # Heuristic: Only trigger people search if question contains likely people-related keywords or patterns
    # (name, email, phone, designation, area, or explicit people query)
    # Also match queries like "how many developers", "number of designers", etc.
    designation_query = None
    general_desig_patterns = [
        r"how many ([\w .,&-]+?)s?(?: (?:are|do|in|at|currently|now|presently|working|work|exist|there|in leapfrog|at leapfrog|in the company|in organization|in org|in team|right now))?\??$",
        r"number of ([\w .,&-]+?)s?(?: (?:are|do|in|at|currently|now|presently|working|work|exist|there|in leapfrog|at leapfrog|in the company|in organization|in org|in team|right now))?\??$",
        r"who are the ([\w .,&-]+?)s?(?: (?:in|at|currently|now|presently|working|work|exist|there|in leapfrog|at leapfrog|in the company|in organization|in org|in team|right now))?\??$",
        r"list of ([\w .,&-]+?)s?(?: (?:in|at|currently|now|presently|working|work|exist|there|in leapfrog|at leapfrog|in the company|in organization|in org|in team|right now))?\??$",
    ]
    for pat in general_desig_patterns:
        m = re.search(pat, lower_q)
        if m:
            designation_query = m.group(1).strip()
            break

    if (
        re.search(r"[\w.]+@[\w.]+", lower_q)
        or re.search(r"\d{7,}", lower_q)
        or "designation" in lower_q
        or "working as" in lower_q
        or re.search(r"who is|contact|about", lower_q)
        or designation_query
    ):
        # Try to extract email
        email_match = re.search(r"[\w.]+@[\w.]+", lower_q)
        if email_match:
            search_term = email_match.group(0)
            matches = [
                p for p in people_data if p.get("email", "").lower() == search_term
            ]
        # Try to extract phone number
        elif re.search(r"\d{7,}", lower_q):
            phone_match = re.search(r"(\+?\d[\d\s-]{6,})", lower_q)
            if phone_match:
                phone = phone_match.group(1).replace(" ", "").replace("-", "")
                matches = [
                    p
                    for p in people_data
                    if p.get("mobilePhone", "").replace(" ", "").replace("-", "")
                    == phone
                ]
            else:
                matches = []
        # Try to extract designation/area
        elif "working as" in lower_q or "designation" in lower_q or designation_query:
            if designation_query:
                desig_area = designation_query.lower()
            else:
                desig_match = re.search(
                    r'(?:working as|designation)\s*(?:an?|the)?\s*"?([\w .,&-]+)"?',
                    lower_q,
                )
                desig_area = desig_match.group(1).strip().lower() if desig_match else ""
            # Remove company references and temporal phrases
            for noise in [
                "in leapfrog",
                "at leapfrog",
                "leapfrog",
                "right now",
                "currently",
                "now",
                "presently",
            ]:
                desig_area = desig_area.replace(noise, "")
            desig_area = desig_area.strip()
            # Remove generic/stop words from query
            stopwords = set(
                [
                    "people",
                    "person",
                    "persons",
                    "who",
                    "how",
                    "many",
                    "number",
                    "of",
                    "the",
                    "are",
                    "is",
                    "in",
                    "at",
                    "as",
                    "working",
                    "work",
                    "do",
                    "there",
                    "currently",
                    "now",
                    "presently",
                    "list",
                    "all",
                    "on",
                    "for",
                    "with",
                    "by",
                    "to",
                    "from",
                    "and",
                    "or",
                    "a",
                    "an",
                    "team",
                    "members",
                    "member",
                ]
            )
            query_words = [
                normalize_word(w)
                for w in re.split(r"[, ]+", desig_area)
                if w and normalize_word(w) not in stopwords
            ]
            matches = []
            for p in people_data:
                designation = p.get("designation", {}).get("name", "").lower()
                area = p.get("designation", {}).get("area", {}).get("name", "").lower()
                combined = f"{designation}, {area}" if area else designation
                combined_words = [
                    normalize_word(w) for w in combined.replace(",", " ").split()
                ]
                # Fuzzy/partial match: any query word in any combined word (or vice versa)
                if any(
                    qw in cw or cw in qw for qw in query_words for cw in combined_words
                ):
                    matches.append(p)
        else:
            name_match = re.search(r"(?:who is|contact|about) ([\w .'-]+)", lower_q)
            search_term = (
                name_match.group(1).strip() if name_match else lower_q.split()[-1]
            )
            matches = get_people_matches(search_term, people_data)
        if not matches:
            return None
        results = []
        if len(matches) > 1:
            results.append(
                f"\033[96m\n================= {len(matches)} result{'s' if len(matches) > 1 else ''} found =================\033[0m\n"
            )
        for idx, person_info in enumerate(matches, 1):
            designation = person_info.get("designation", {}).get("name", "N/A")
            area = person_info.get("designation", {}).get("area", {}).get("name", None)
            designation_area = f"{designation}, {area}" if area else designation
            info_lines = [
                f"\033[92m[{idx}] {person_info.get('firstName', '').title()} {person_info.get('middleName', '') or ''}{person_info.get('lastName', '').title()}\033[0m",
                f"   \033[94mEmail:\033[0m {person_info.get('email', 'N/A')}",
                f"   \033[94mMobile:\033[0m {person_info.get('mobilePhone', 'N/A')}",
                f"   \033[94mDepartment:\033[0m {person_info.get('department', {}).get('name', 'N/A')}",
                f"   \033[94mDesignation:\033[0m {designation_area}",
                f"   \033[93mMore info:\033[0m https://vyaguta.lftechnology.com/leapfroggers/{person_info.get('id', '')}",
            ]
            results.append("\n".join(info_lines))
            if len(matches) > 1 and idx != len(matches):
                results.append("\033[90m" + ("-" * 50) + "\033[0m")
        return "\n".join(results)
    # If not a people-related query, return None so main.py can use RAG/LLM
    return None


def get_people_matches(name_or_email, people_data):
    """
    Returns a list of all people matching the name or email (normalized, partial or full).
    Args:
        name_or_email (str): Name or email to search for.
        people_data (list): List of people dicts.
    Returns:
        list: List of matching person dicts (can be empty).
    """
    import re
    import urllib.parse

    def normalize(s):
        return re.sub(r"\s+", " ", s.strip().lower())

    name_or_email = normalize(name_or_email)
    encoded_name = urllib.parse.quote_plus(name_or_email)
    matches = []

    # Exact email match
    for person in people_data:
        if person.get("email", "").lower() == name_or_email:
            matches.append(person)

    # Exact full name match (collapse spaces in both)
    for person in people_data:
        full_name = f"{person.get('firstName', '')} {person.get('middleName', '') or ''} {person.get('lastName', '')}"
        full_name_norm = normalize(full_name)
        full_name_nospaces = full_name_norm.replace(" ", "")
        # Also try matching ignoring middle name if present
        full_name_no_middle = (
            f"{person.get('firstName', '')} {person.get('lastName', '')}"
        )
        full_name_no_middle_norm = normalize(full_name_no_middle)
        if (
            name_or_email == full_name_norm
            or name_or_email == full_name_nospaces
            or name_or_email == full_name_no_middle_norm
            or encoded_name == urllib.parse.quote_plus(full_name_norm)
            or encoded_name == urllib.parse.quote_plus(full_name_no_middle_norm)
        ):
            if person not in matches:
                matches.append(person)

    # Partial match (first, middle, or last name, or first+last)
    for person in people_data:
        names = [
            normalize(person.get("firstName", "")),
            normalize(person.get("middleName", "")) if person.get("middleName") else "",
            normalize(person.get("lastName", "")),
        ]
        # Add first+last as a partial match
        first_last = normalize(
            f"{person.get('firstName', '')} {person.get('lastName', '')}"
        )
        if any(name_or_email in n for n in names if n) or name_or_email in first_last:
            if person not in matches:
                matches.append(person)
    return matches


import requests


def fetch_people_data():
    """
    Fetches the latest people data from the Vyaguta API.
    Returns:
        list: List of people dictionaries with selected fields.
    """
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
            # If the API provides total pages, use it for efficiency
            meta = data.get("meta", {})
            total_pages = meta.get("totalPages")
            if total_pages and page >= total_pages:
                break
            page += 1
        except Exception as e:
            print(f"Warning: Could not fetch people data from API (page {page}). {e}")
            break
    return all_people


def get_person_info(name_or_email, people_data):
    """
    Searches for a person by name or email in the people data.
    Args:
        name_or_email (str): Name or email to search for.
        people_data (list): List of people dicts.
    Returns:
        dict or None: Person dict if found, else None.
    """
    import re
    import urllib.parse

    # Normalize input: lowercase, strip, collapse multiple spaces to one
    def normalize(s):
        return re.sub(r"\s+", " ", s.strip().lower())

    name_or_email = normalize(name_or_email)
    encoded_name = urllib.parse.quote_plus(name_or_email)

    # Try exact email match
    for person in people_data:
        if person.get("email", "").lower() == name_or_email:
            return person

    # Try exact full name match (collapse spaces in both)
    for person in people_data:
        full_name = f"{person.get('firstName', '')} {person.get('middleName', '') or ''} {person.get('lastName', '')}"
        full_name_norm = normalize(full_name)
        full_name_nospaces = full_name_norm.replace(" ", "")
        if (
            name_or_email == full_name_norm
            or name_or_email == full_name_nospaces
            or encoded_name == urllib.parse.quote_plus(full_name_norm)
        ):
            return person

    # Try partial match (first, middle, or last name)
    for person in people_data:
        names = [
            normalize(person.get("firstName", "")),
            normalize(person.get("middleName", "")) if person.get("middleName") else "",
            normalize(person.get("lastName", "")),
        ]
        if any(name_or_email in n for n in names if n):
            return person
    return None
