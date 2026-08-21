import re


# ============================================================
# KEYWORD GROUPS
# ============================================================

KEYWORD_GROUPS = {

    # Programming
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++"],
    "c#": ["c#", "c sharp"],

    # Java
    "spring boot": ["spring boot"],
    "spring": ["spring"],
    "spring mvc": ["spring mvc"],
    "spring security": ["spring security"],
    "hibernate": ["hibernate"],
    "jpa": ["jpa"],
    "maven": ["maven"],
    "gradle": ["gradle"],
    "junit": ["junit"],
    "mockito": ["mockito"],

    # Python
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi", "fast api"],
    "pytest": ["pytest"],

    # Web
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs", "vue.js"],
    "node.js": ["node", "nodejs", "node.js"],

    # API
    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest api development"
    ],

    "graphql": ["graphql"],

    # Database
    "sql": [
        "sql",
        "structured query language"
    ],

    "mysql": ["mysql"],

    "postgresql": [
        "postgresql",
        "postgres"
    ],

    "mongodb": [
        "mongodb",
        "mongo db"
    ],

    "oracle": [
        "oracle database",
        "oracle db"
    ],

    "sqlite": ["sqlite"],
    "redis": ["redis"],

    # Version control
    "git": ["git"],

    "github": [
        "github",
        "github.com"
    ],

    "gitlab": ["gitlab"],
    "bitbucket": ["bitbucket"],

    "version control": [
        "version control",
        "version control system",
        "version control systems"
    ],

    # DevOps
    "docker": ["docker"],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "jenkins": ["jenkins"],

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment"
    ],

    "terraform": ["terraform"],
    "ansible": ["ansible"],

    "github actions": [
        "github actions"
    ],

    # Cloud
    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "gcp": [
        "gcp",
        "google cloud",
        "google cloud platform"
    ],

    # Data Science
    "pandas": ["pandas"],
    "numpy": ["numpy"],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],

    # AI / ML
    "machine learning": [
        "machine learning",
        "machine-learning"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning"
    ],

    "artificial intelligence": [
        "artificial intelligence"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision"
    ],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],

    # Computer Science
    "data structures": [
        "data structures",
        "data structure",
        "data structures and algorithms",
        "data structure and algorithms",
        "data structures & algorithms"
    ],

    "algorithms": [
        "algorithms",
        "algorithm",
        "data structures and algorithms",
        "data structure and algorithms",
        "data structures & algorithms"
    ],

    "object oriented programming": [
        "object oriented programming",
        "object-oriented programming",
        "oop"
    ],

    "design patterns": [
        "design patterns",
        "design pattern"
    ],

    "problem solving": [
        "problem solving",
        "problem-solving"
    ],

    "system design": [
        "system design"
    ],

    # Testing
    "unit testing": [
        "unit testing",
        "unit test",
        "unit tests"
    ],

    "integration testing": [
        "integration testing",
        "integration test",
        "integration tests"
    ],

    "selenium": ["selenium"],
    "cypress": ["cypress"],
    "postman": ["postman"],

    # Methodologies
    "agile": ["agile"],
    "scrum": ["scrum"],
    "kanban": ["kanban"]
}


# ============================================================
# NORMALIZE
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# EXTRACT KEYWORDS
# ============================================================

def extract_keywords(text):

    text = normalize_text(text)

    if not text:
        return set()

    found = set()


    # --------------------------------------------------------
    # Standard keyword matching
    # --------------------------------------------------------

    for keyword, aliases in KEYWORD_GROUPS.items():

        for alias in aliases:

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text
            ):

                found.add(keyword)

                break


    # --------------------------------------------------------
    # DSA detection
    # --------------------------------------------------------

    dsa_patterns = [

        r"\bdata\s+structures?\s+and\s+algorithms?\b",

        r"\bdata\s+structures?\s*&\s*algorithms?\b",

        r"\bdsa\b"
    ]

    for pattern in dsa_patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found.add("data structures")
            found.add("algorithms")

            break


    # --------------------------------------------------------
    # Remove generic parent keywords
    # --------------------------------------------------------

    if "spring boot" in found:
        found.discard("spring")

    if "rest api" in found:
        found.discard("api")


    return found


# ============================================================
# KEYWORD SCORE
# ============================================================

def calculate_keyword_score(
    resume_text,
    job_description
):

    resume_keywords = extract_keywords(
        resume_text
    )

    job_keywords = extract_keywords(
        job_description
    )

    if not job_keywords:

        return 0, [], []


    matching_keywords = (
        resume_keywords
        & job_keywords
    )

    missing_keywords = (
        job_keywords
        - resume_keywords
    )


    score = round(
        (
            len(matching_keywords)
            /
            len(job_keywords)
        )
        * 100
    )


    return (
        score,
        sorted(matching_keywords),
        sorted(missing_keywords)
    )