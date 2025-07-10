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
    import urllib.parse

    def normalize(s):
        return re.sub(r"\s+", " ", s.strip().lower())

    name_or_email = normalize(name_or_email)
    encoded_name = urllib.parse.quote_plus(name_or_email)
    matches = []
    for person in people_data:
        if person.get("email", "").lower() == name_or_email:
            matches.append(person)
    for person in people_data:
        full_name = f"{person.get('firstName', '')} {person.get('middleName', '') or ''} {person.get('lastName', '')}"
        full_name_norm = normalize(full_name)
        full_name_nospaces = full_name_norm.replace(" ", "")
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
    for person in people_data:
        names = [
            normalize(person.get("firstName", "")),
            normalize(person.get("middleName", "")) if person.get("middleName") else "",
            normalize(person.get("lastName", "")),
        ]
        first_last = normalize(
            f"{person.get('firstName', '')} {person.get('lastName', '')}"
        )
        if any(name_or_email in n for n in names if n) or name_or_email in first_last:
            if person not in matches:
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
    # 2. Fuzzy matching for people
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
    # 3. Try to extract email, phone, or name
    matches = []
    email_match = re.search(r"[\w.]+@[\w.]+", lower_q)
    if email_match:
        search_term = email_match.group(0)
        matches = [p for p in people_data if p.get("email", "").lower() == search_term]
    elif re.search(r"\d{7,}", lower_q):
        phone_match = re.search(r"(\+?\d[\d\s-]{6,})", lower_q)
        if phone_match:
            phone = phone_match.group(1).replace(" ", "").replace("-", "")
            matches = [
                p
                for p in people_data
                if p.get("mobilePhone", "").replace(" ", "").replace("-", "") == phone
            ]
    elif "working as" in lower_q or "designation" in lower_q or designation_query:
        if designation_query:
            desig_area = designation_query.lower()
        else:
            desig_match = re.search(
                r'(?:working as|designation)\s*(?:an?|the)?\s*"?([\w .,&-]+)"?', lower_q
            )
            desig_area = desig_match.group(1).strip().lower() if desig_match else ""
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
        for p in people_data:
            designation = p.get("designation", {}).get("name", "").lower()
            area = p.get("designation", {}).get("area", {}).get("name", "").lower()
            combined = f"{designation}, {area}" if area else designation
            combined_words = [
                normalize_word(w) for w in combined.replace(",", " ").split()
            ]
            if any(qw in cw or cw in qw for qw in query_words for cw in combined_words):
                matches.append(p)
    else:
        # Improved name extraction for queries like "Purna's birthday?", "When was Purna born?", "Where does Purna live?"
        name_match = re.search(r"(?:who is|contact|about) ([\w .'-]+)", lower_q)
        if name_match:
            search_term = name_match.group(1).strip()
        else:
            # Try to extract name after 'of', 'for', or at the end (capitalized)
            name_match2 = re.search(
                r"(?:of|for|does|is|was|did|has|have|had|will|can|could|would|should|where|when|what|who|whom|whose|which|how) ([A-Z][a-zA-Z .'-]+)",
                question,
            )
            if name_match2:
                search_term = name_match2.group(1).strip()
            else:
                # Try to extract the last capitalized word(s) at the end
                name_match3 = re.findall(r"([A-Z][a-zA-Z .'-]+)", question)
                if name_match3:
                    search_term = name_match3[-1].strip()
                else:
                    # Remove possessive 's and punctuation
                    search_term = lower_q
                    search_term = re.sub(r"'s\\b", "", search_term)
                    search_term = re.sub(r"[^a-zA-Z0-9 .'-]", "", search_term)
                    # Remove known keywords (but only as whole words)
                    for kw in [
                        "birthday",
                        "birth date",
                        "date of birth",
                        "born",
                        "availability",
                        "availibility",
                        "available time",
                        "joining date",
                        "address",
                        "location",
                        "employee since",
                        "gender",
                        "blood group",
                        "country",
                        "timezone",
                        "shift",
                        "type",
                        "experience",
                        "working shift",
                        "working type",
                        "working hour",
                        "working hours",
                        "working time",
                        "what is the",
                        "when was",
                        "who is",
                        "of",
                        "the",
                        "a",
                        "an",
                        "is",
                        "was",
                        "in",
                        "on",
                        "at",
                        "for",
                        "with",
                        "to",
                        "from",
                        "does",
                        "live",
                        "where",
                    ]:
                        search_term = re.sub(rf"\\b{re.escape(kw)}\\b", "", search_term)
                    search_term = search_term.strip()
                    # If nothing left, fallback to last word in original question
                    if not search_term:
                        words = lower_q.split()
                        if words:
                            search_term = words[-1]
        print("[DEBUG] Name search term:", search_term)
        matches = get_people_matches(search_term, people_data)
        # If no matches and search_term has multiple words, try the last word (likely the name)
        if not matches and len(search_term.split()) > 1:
            last_word = search_term.split()[-1]
            stopwords = {
                "is",
                "the",
                "of",
                "a",
                "an",
                "in",
                "on",
                "at",
                "for",
                "with",
                "to",
                "from",
                "what",
                "when",
                "who",
                "gender",
                "birthday",
                "born",
                "does",
                "live",
                "where",
            }
            if last_word not in stopwords:
                matches = get_people_matches(last_word, people_data)
                if matches:
                    print(f"[DEBUG] Fallback match found for last word: {last_word}")
        # Only if still no matches, try each word (excluding stopwords)
        if not matches and len(search_term.split()) > 1:
            for word in search_term.split():
                if word in stopwords:
                    continue
                matches = get_people_matches(word, people_data)
                if matches:
                    print(f"[DEBUG] Fallback match found for word: {word}")
                    break
    if not matches:
        print("[DEBUG] No matches found for people.")
        return None
    # If multiple matches, show disambiguation list and prompt for clarification
    if len(matches) > 1:
        disambig_lines = [
            f"Multiple people found matching your query. Please specify which one you mean:\n"
        ]
        for idx, person in enumerate(matches, 1):
            full_name = f"{person.get('firstName', '').title()} {person.get('middleName', '') or ''}{person.get('lastName', '').title()}"
            email = person.get("email", "N/A")
            designation = person.get("designation", {}).get("name", "N/A")
            disambig_lines.append(
                f"[{idx}] {full_name} | Email: {email} | Designation: {designation}"
            )
        return "\n".join(disambig_lines)
    # 4. If the question is about detailed info, fetch from detailed API
    detail_keywords = [
        "birthday",
        "birth date",
        "date of birth",
        "born",
        "availability",
        "availibility",
        "available time",
        "joining date",
        "address",
        "location",
        "employee since",
        "gender",
        "blood group",
        "country",
        "timezone",
        "shift",
        "type",
        "experience",
        "working shift",
        "working type",
        "working hour",
        "working hours",
        "working time",
        "live",
        "reside",
        "home",
        "where",
    ]
    if any(k in lower_q for k in detail_keywords):
        print("[DEBUG] Entering detailed info block for:", question)
        responses = []
        for person_info in matches:
            person_id = person_info.get("id")
            if not person_id:
                continue
            details = fetch_person_details_by_id(person_id)
            if not details:
                responses.append(
                    f"Sorry, I couldn't fetch more details for {person_info.get('firstName', '').title()}."
                )
                continue
            # Map question to fields
            data = details.get("data", details)  # Use 'data' key if present, else root
            if any(
                k in lower_q
                for k in ["birthday", "birth date", "date of birth", "born"]
            ):
                birthday = data.get("birthday") or data.get("dateOfBirth")
                if birthday:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s birthday is on {birthday}."
                    )
                else:
                    responses.append("Birthday information is not available.")
            if any(
                k in lower_q for k in ["availability", "availibility", "available time"]
            ):
                availability = data.get("availabilityTime") or data.get("availability")
                if availability:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s availability time: {availability}."
                    )
                else:
                    responses.append("Availability information is not available.")
            if any(k in lower_q for k in ["joining date", "employee since"]):
                joining = (
                    data.get("employeeSince")
                    or data.get("joiningDate")
                    or data.get("joinDate")
                )
                if joining:
                    responses.append(
                        f"{data.get('firstName', '').title()} joined on {joining}."
                    )
                else:
                    responses.append("Joining date is not available.")
            if any(
                k in lower_q
                for k in [
                    "address",
                    "location",
                    "country",
                    "live",
                    "reside",
                    "home",
                    "where",
                ]
            ):
                address = (
                    data.get("address")
                    or data.get("location")
                    or data.get("country")
                    or data.get("permanentAddress")
                    or data.get("temporaryAddress")
                )
                if address:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s address: {address}."
                    )
                else:
                    responses.append("Address/location information is not available.")
            if any(k in lower_q for k in ["gender"]):
                gender = data.get("gender")
                if gender:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s gender: {gender.title()}."
                    )
                else:
                    responses.append("Gender information is not available.")
            if any(k in lower_q for k in ["blood group"]):
                blood = data.get("bloodGroup")
                if blood:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s blood group: {blood}."
                    )
                else:
                    responses.append("Blood group information is not available.")
            if any(k in lower_q for k in ["timezone"]):
                tz = data.get("timezone")
                if tz:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s timezone: {tz}."
                    )
                else:
                    responses.append("Timezone information is not available.")
            if any(
                k in lower_q
                for k in [
                    "shift",
                    "working shift",
                    "working hour",
                    "working hours",
                    "working time",
                ]
            ):
                shift = (
                    data.get("workingShift")
                    or data.get("shift")
                    or data.get("workingHour")
                    or data.get("workingHours")
                    or data.get("workingTime")
                )
                if shift:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s working shift: {shift}."
                    )
                else:
                    responses.append("Working shift/hour information is not available.")
            if any(k in lower_q for k in ["type", "working type"]):
                wtype = (
                    data.get("workingType")
                    or data.get("type")
                    or data.get("scheduledType")
                )
                if wtype:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s working type: {wtype}."
                    )
                else:
                    responses.append("Working type information is not available.")
            if any(k in lower_q for k in ["experience", "previous experience"]):
                exp = (
                    data.get("previousExperience")
                    or data.get("experience")
                    or data.get("pastExperience")
                )
                if exp:
                    responses.append(
                        f"{data.get('firstName', '').title()}'s previous experience: {exp}."
                    )
                else:
                    responses.append(
                        "Previous experience information is not available."
                    )
        if responses:
            return "\n".join(responses)
        else:
            return "I found more details, but I'm not sure what information you need."
    # 5. Otherwise, return basic info (list style)
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
