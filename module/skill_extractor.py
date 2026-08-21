import re


# ============================================================
# SKILL GROUPS
# ============================================================

SKILL_GROUPS = {

    # --------------------------------------------------------
    # Programming Languages
    # --------------------------------------------------------

    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "javascript": [
        "javascript",
        "js"
    ],

    "typescript": [
        "typescript",
        "ts"
    ],

    "c++": [
        "c++"
    ],

    "c#": [
        "c#",
        "c sharp"
    ],

    # --------------------------------------------------------
    # Web Technologies
    # --------------------------------------------------------

    "html": [
        "html",
        "html5"
    ],

    "css": [
        "css",
        "css3"
    ],

    "react": [
        "react",
        "reactjs",
        "react.js"
    ],

    "angular": [
        "angular",
        "angularjs"
    ],

    "vue": [
        "vue",
        "vuejs",
        "vue.js"
    ],

    "node.js": [
        "node",
        "nodejs",
        "node.js"
    ],

    # --------------------------------------------------------
    # Java Technologies
    # --------------------------------------------------------

    "spring boot": [
        "spring boot"
    ],

    "spring": [
        "spring"
    ],

    "spring mvc": [
        "spring mvc"
    ],

    "spring security": [
        "spring security"
    ],

    "hibernate": [
        "hibernate"
    ],

    "jpa": [
        "jpa"
    ],

    "maven": [
        "maven"
    ],

    "gradle": [
        "gradle"
    ],

    "junit": [
        "junit"
    ],

    "mockito": [
        "mockito"
    ],

    # --------------------------------------------------------
    # Python Frameworks
    # --------------------------------------------------------

    "django": [
        "django"
    ],

    "flask": [
        "flask"
    ],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "pytest": [
        "pytest"
    ],

    # --------------------------------------------------------
    # APIs
    # --------------------------------------------------------

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    ],

    "graphql": [
        "graphql"
    ],

    # --------------------------------------------------------
    # Databases
    # --------------------------------------------------------

    "sql": [
        "sql",
        "structured query language"
    ],

    "mysql": [
        "mysql"
    ],

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

    "sqlite": [
        "sqlite"
    ],

    "redis": [
        "redis"
    ],

    # --------------------------------------------------------
    # Version Control
    # --------------------------------------------------------

    "git": [
        "git"
    ],

    "github": [
        "github"
    ],

    "gitlab": [
        "gitlab"
    ],

    "bitbucket": [
        "bitbucket"
    ],

    "version control": [
        "version control",
        "version control system",
        "version control systems"
    ],

    # --------------------------------------------------------
    # DevOps
    # --------------------------------------------------------

    "docker": [
        "docker"
    ],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "jenkins": [
        "jenkins"
    ],

    "ci/cd": [
        "ci/cd",
        "ci cd",
        "continuous integration",
        "continuous delivery",
        "continuous deployment"
    ],

    "terraform": [
        "terraform"
    ],

    "ansible": [
        "ansible"
    ],

    "github actions": [
        "github actions"
    ],

    # --------------------------------------------------------
    # Cloud
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Data Science
    # --------------------------------------------------------

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "matplotlib": [
        "matplotlib"
    ],

    "seaborn": [
        "seaborn"
    ],

    # --------------------------------------------------------
    # AI / ML
    # --------------------------------------------------------

    "machine learning": [
        "machine learning",
        "machine-learning"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "artificial-intelligence",
        "ai"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "keras": [
        "keras"
    ],

    # --------------------------------------------------------
    # Computer Science
    # --------------------------------------------------------

    "data structures": [
        "data structures",
        "data structure"
    ],

    "algorithms": [
        "algorithms",
        "algorithm"
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

    # --------------------------------------------------------
    # Testing
    # --------------------------------------------------------

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

    "selenium": [
        "selenium"
    ],

    "cypress": [
        "cypress"
    ],

    "postman": [
        "postman"
    ],

    # --------------------------------------------------------
    # Methodologies
    # --------------------------------------------------------

    "agile": [
        "agile"
    ],

    "scrum": [
        "scrum"
    ],

    "kanban": [
        "kanban"
    ]
}


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = text.lower()

    # --------------------------------------------------------
    # Normalize dash characters
    # --------------------------------------------------------

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("-", "-")

    # --------------------------------------------------------
    # Normalize HTML
    # --------------------------------------------------------

    text = re.sub(
        r"\bhtml\s*5\b",
        "html",
        text
    )

    # --------------------------------------------------------
    # Normalize CSS
    # --------------------------------------------------------

    text = re.sub(
        r"\bcss\s*3\b",
        "css",
        text
    )

    # --------------------------------------------------------
    # Normalize REST API
    # --------------------------------------------------------

    text = re.sub(
        r"\brestful\s+apis?\b",
        "rest api",
        text
    )

    text = re.sub(
        r"\brest\s+apis?\b",
        "rest api",
        text
    )

    # --------------------------------------------------------
    # Normalize FastAPI
    # --------------------------------------------------------

    text = re.sub(
        r"\bfast\s+api\b",
        "fastapi",
        text
    )

    # --------------------------------------------------------
    # Normalize CI/CD
    # --------------------------------------------------------

    text = re.sub(
        r"\bci\s*/?\s*cd\b",
        "ci/cd",
        text
    )

    # --------------------------------------------------------
    # Normalize multiple spaces
    # --------------------------------------------------------

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FIND SKILLS
# ============================================================

def extract_skills(text):

    text = normalize_text(text)

    if not text:
        return []

    found_skills = set()

    # --------------------------------------------------------
    # Search every skill and its aliases
    # --------------------------------------------------------

    for skill, aliases in SKILL_GROUPS.items():

        for alias in aliases:

            alias = alias.lower().strip()

            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text
            ):

                found_skills.add(skill)

                break

    # --------------------------------------------------------
    # Remove generic skills when specific skills exist
    # --------------------------------------------------------

    if "spring boot" in found_skills:
        found_skills.discard("spring")

    if "spring mvc" in found_skills:
        found_skills.discard("spring")

    if "spring security" in found_skills:
        found_skills.discard("spring")

    # --------------------------------------------------------
    # Return sorted list
    # --------------------------------------------------------

    return sorted(found_skills)