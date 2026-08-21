import re


# ============================================================
# SECTION ALIASES
# ============================================================

SECTION_ALIASES = {

    "contact": [
        "contact",
        "contact information",
        "personal information",
        "personal details"
    ],

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "career summary",
        "career objective",
        "objective",
        "about me"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "skills technologies",
        "skills and technologies",
        "technical knowledge",
        "technologies"
    ],

    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
        "qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "employment history",
        "work history",
        "career history",
        "internship",
        "internships",
        "internship experience"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "major projects",
        "key projects"
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "courses",
        "licenses",
        "licenses certifications"
    ],

    "achievements": [
        "achievements",
        "achievement",
        "awards",
        "honors",
        "honours",
        "accomplishments"
    ],

    "coding_profiles": [
        "coding profiles",
        "coding profile",
        "coding platforms",
        "coding platform",
        "competitive programming",
        "competitive programming profiles",
        "programming profiles",
        "online profiles"
    ]
}


# ============================================================
# ALL SECTION NAMES
# ============================================================

SECTION_NAMES = [

    "contact",

    "summary",

    "skills",

    "education",

    "experience",

    "projects",

    "certifications",

    "achievements",

    "coding_profiles"
]


# ============================================================
# REQUIRED SECTIONS
# ============================================================
#
# Professional Summary and Achievements are OPTIONAL.
#
# They are NOT included in the section score.
# ============================================================

REQUIRED_SECTION_NAMES = [

    "contact",

    "skills",

    "education",

    "experience",

    "projects",

    "certifications",

    "coding_profiles"
]


# ============================================================
# NORMALIZE LINE
# ============================================================

def normalize_line(line):

    if not line:
        return ""

    line = str(line).strip()

    # Remove bullets
    line = re.sub(
        r"^[•●▪◦\-*]+\s*",
        "",
        line
    )

    # Remove numbering
    line = re.sub(
        r"^\d+[\.\)]\s*",
        "",
        line
    )

    # Normalize spaces
    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


# ============================================================
# NORMALIZE SECTION HEADING
# ============================================================

def normalize_heading(line):

    line = normalize_line(line)

    if not line:
        return ""

    line = line.lower()

    # Replace separators
    line = re.sub(
        r"[:|]",
        " ",
        line
    )

    # Keep letters, numbers, + and #
    line = re.sub(
        r"[^a-z0-9+#]+",
        " ",
        line
    )

    # Normalize spaces
    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


# ============================================================
# COMPACT HEADING
# ============================================================

def compact_heading(line):

    heading = normalize_heading(line)

    return heading.replace(
        " ",
        ""
    )


# ============================================================
# DETECT SECTION HEADING
# ============================================================

def detect_section_heading(line):

    heading = normalize_heading(line)

    if not heading:
        return None

    compact = compact_heading(line)

    for section_name, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            alias_normalized = normalize_heading(
                alias
            )

            alias_compact = alias_normalized.replace(
                " ",
                ""
            )

            # Normal match
            if heading == alias_normalized:

                return section_name

            # PDF extraction match
            #
            # PROFESSIONALSUMMARY
            #
            # becomes
            #
            # professionalsummary
            #
            if compact == alias_compact:

                return section_name

    return None


# ============================================================
# CONTACT INFORMATION
# ============================================================

def detect_contact_information(text):

    if not text:
        return []

    contact_lines = []

    for line in text.splitlines():

        line = normalize_line(line)

        if not line:
            continue

        # ----------------------------------------------------
        # Ignore very short numeric lines
        # ----------------------------------------------------

        if re.fullmatch(
            r"\d+",
            line
        ):
            continue

        # ----------------------------------------------------
        # Email
        # ----------------------------------------------------

        if re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            line
        ):

            contact_lines.append(line)

            continue

        # ----------------------------------------------------
        # Phone
        # ----------------------------------------------------

        if re.search(
            r"(\+?\d[\d\s().-]{7,}\d)",
            line
        ):

            contact_lines.append(line)

            continue

        # ----------------------------------------------------
        # LinkedIn URL
        # ----------------------------------------------------

        if re.search(
            r"linkedin\.com",
            line,
            re.IGNORECASE
        ):

            contact_lines.append(line)

            continue

        # ----------------------------------------------------
        # GitHub URL
        # ----------------------------------------------------

        if re.search(
            r"github\.com",
            line,
            re.IGNORECASE
        ):

            contact_lines.append(line)

            continue

        # ----------------------------------------------------
        # Website
        # ----------------------------------------------------

        if re.search(
            r"(https?://|www\.)",
            line,
            re.IGNORECASE
        ):

            contact_lines.append(line)

    return list(
        dict.fromkeys(contact_lines)
    )


# ============================================================
# CODING PROFILES
# ============================================================

def detect_coding_profiles(text):

    if not text:
        return []

    coding_lines = []

    for line in text.splitlines():

        line = normalize_line(line)

        if not line:
            continue

        # ----------------------------------------------------
        # Ignore numbers
        # ----------------------------------------------------

        if re.fullmatch(
            r"\d+",
            line
        ):
            continue

        # ----------------------------------------------------
        # LeetCode
        # ----------------------------------------------------

        if re.search(
            r"\bleet\s*code\b",
            line,
            re.IGNORECASE
        ):

            coding_lines.append(line)

            continue

        # ----------------------------------------------------
        # HackerRank
        # ----------------------------------------------------

        if re.search(
            r"\bhacker\s*rank\b",
            line,
            re.IGNORECASE
        ):

            coding_lines.append(line)

            continue

        # ----------------------------------------------------
        # CodeChef
        # ----------------------------------------------------

        if re.search(
            r"\bcode\s*chef\b",
            line,
            re.IGNORECASE
        ):

            coding_lines.append(line)

            continue

        # ----------------------------------------------------
        # GeeksForGeeks
        # ----------------------------------------------------

        if re.search(
            r"\bgeeks\s*for\s*geeks\b",
            line,
            re.IGNORECASE
        ):

            coding_lines.append(line)

            continue

        # ----------------------------------------------------
        # InterviewBit
        # ----------------------------------------------------

        if re.search(
            r"\binterview\s*bit\b",
            line,
            re.IGNORECASE
        ):

            coding_lines.append(line)

            continue

    return list(
        dict.fromkeys(coding_lines)
    )


# ============================================================
# DETECT SECTIONS
# ============================================================

def detect_sections(text):

    sections = {

        "contact": [],

        "summary": [],

        "skills": [],

        "education": [],

        "experience": [],

        "projects": [],

        "certifications": [],

        "achievements": [],

        "coding_profiles": []
    }

    if not text:

        return sections

    # ========================================================
    # PREPARE LINES
    # ========================================================

    raw_lines = text.splitlines()

    lines = []

    for line in raw_lines:

        clean = normalize_line(line)

        if clean:

            lines.append(clean)

    # ========================================================
    # CONTACT
    # ========================================================

    sections["contact"].extend(
        detect_contact_information(text)
    )

    # ========================================================
    # CODING PROFILES
    # ========================================================

    sections["coding_profiles"].extend(
        detect_coding_profiles(text)
    )

    # ========================================================
    # SECTION DETECTION
    # ========================================================

    current_section = None

    for line in lines:

        detected_section = detect_section_heading(
            line
        )

        # ----------------------------------------------------
        # New section
        # ----------------------------------------------------

        if detected_section:

            current_section = detected_section

            continue

        # ----------------------------------------------------
        # Add content to current section
        # ----------------------------------------------------

        if current_section:

            sections[current_section].append(
                line
            )

    # ========================================================
    # REMOVE ACCIDENTAL CODING PROFILE NUMBERS
    # ========================================================

    cleaned_coding_profiles = []

    for line in sections["coding_profiles"]:

        if re.fullmatch(
            r"\d+",
            line
        ):
            continue

        cleaned_coding_profiles.append(line)

    sections["coding_profiles"] = (
        cleaned_coding_profiles
    )

    # ========================================================
    # REMOVE ACCIDENTAL SECTION HEADING LEAKAGE
    # ========================================================

    for section_name in SECTION_NAMES:

        cleaned = []

        for line in sections[section_name]:

            if detect_section_heading(line):

                continue

            cleaned.append(line)

        sections[section_name] = cleaned

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    for section_name in sections:

        sections[section_name] = list(
            dict.fromkeys(
                sections[section_name]
            )
        )

    return sections


# ============================================================
# SECTION SCORE
# ============================================================
#
# Professional Summary -> OPTIONAL
# Achievements         -> OPTIONAL
#
# Therefore they are NOT counted.
# ============================================================

def calculate_section_score(sections):

    if not sections:

        return 0

    found_sections = 0

    for section_name in REQUIRED_SECTION_NAMES:

        content = sections.get(
            section_name,
            []
        )

        if content:

            found_sections += 1

    total_required_sections = len(
        REQUIRED_SECTION_NAMES
    )

    if total_required_sections == 0:

        return 0

    return round(
        (
            found_sections
            / total_required_sections
        ) * 100
    )