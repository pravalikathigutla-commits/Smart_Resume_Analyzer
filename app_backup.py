from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

from module.resume_parser import extract_resume_text
from module.skill_extractor import extract_skills
from module.keyword_matcher import calculate_keyword_score
from module.resume_matcher import calculate_match
from module.resume_sections import detect_sections
from module.ats_scorer import calculate_ats_score


app = FastAPI(title="Smart Resume Analyzer")


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Smart Resume Analyzer</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                margin: 0;
                padding: 40px;
            }

            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            h1 {
                color: #222;
            }

            input, textarea, button {
                width: 100%;
                margin-top: 10px;
                margin-bottom: 20px;
                padding: 12px;
                box-sizing: border-box;
            }

            button {
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background: #1d4ed8;
            }

            #result {
                margin-top: 20px;
                white-space: pre-wrap;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🚀 Smart Resume Analyzer</h1>

            <p>
                Upload your resume and compare it with a job description.
            </p>

            <form id="resumeForm">

                <label><b>Resume (PDF/DOCX)</b></label>

                <input
                    type="file"
                    id="resume"
                    name="file"
                    accept=".pdf,.docx"
                    required
                >

                <label><b>Job Description</b></label>

                <textarea
                    id="job_description"
                    name="job_description"
                    rows="10"
                    placeholder="Paste the job description here..."
                    required
                ></textarea>

                <button type="submit">
                    Upload & Analyze
                </button>

            </form>

            <div id="result"></div>

        </div>


        <script>

            document
                .getElementById("resumeForm")
                .addEventListener("submit", async function(event) {

                    event.preventDefault();

                    const formData = new FormData();

                    const file =
                        document.getElementById("resume").files[0];

                    const jobDescription =
                        document.getElementById("job_description").value;

                    formData.append("file", file);

                    formData.append(
                        "job_description",
                        jobDescription
                    );

                    document.getElementById("result").innerHTML =
                        "⏳ Analyzing resume...";

                    try {

                        const response = await fetch(
                            "/analyze",
                            {
                                method: "POST",
                                body: formData
                            }
                        );

                        const data = await response.json();

                        document.getElementById("result").innerHTML =
                            "<h2>📊 ATS Analysis</h2>" +

                            "<p><b>ATS Score:</b> " +
                            data.ats_score +
                            "/100</p>" +

                            "<p><b>Skill Score:</b> " +
                            data.skill_score +
                            "/100</p>" +

                            "<p><b>Section Score:</b> " +
                            data.section_score +
                            "/100</p>" +

                            "<p><b>Keyword Score:</b> " +
                            data.keyword_score +
                            "/100</p>" +

                            "<p><b>Resume Skills:</b><br>" +
                            data.resume_skills.join(", ") +
                            "</p>" +

                            "<p><b>Matching Skills:</b><br>" +
                            data.matching_skills.join(", ") +
                            "</p>" +

                            "<p><b>Missing Skills:</b><br>" +
                            data.missing_skills.join(", ") +
                            "</p>" +

                            "<p><b>Matching Keywords:</b><br>" +
                            data.matching_keywords.join(", ") +
                            "</p>" +

                            "<p><b>Missing Keywords:</b><br>" +
                            data.missing_keywords.join(", ") +
                            "</p>";

                    } catch (error) {

                        document.getElementById("result").innerHTML =
                            "❌ Error: " + error;

                    }

                });

        </script>

    </body>
    </html>
    """


# ============================================================
# ANALYZE RESUME
# ============================================================

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    filename = file.filename.lower()

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):

        return {
            "error":
            "Unsupported file type. Please upload PDF or DOCX."
        }


    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    contents = await file.read()


    # --------------------------------------------------------
    # Extract resume text
    # --------------------------------------------------------

    import io

    file_object = io.BytesIO(contents)

    resume_text = extract_resume_text(
        file_object,
        file.filename
    )


    # --------------------------------------------------------
    # Extract skills from resume
    # --------------------------------------------------------

    resume_skills = extract_skills(
        resume_text
    )


    # --------------------------------------------------------
    # Extract skills from job description
    # --------------------------------------------------------

    job_skills = extract_skills(
        job_description
    )


    # --------------------------------------------------------
    # Match resume skills with job skills
    # --------------------------------------------------------

    skill_score, matching_skills, missing_skills = calculate_match(
        resume_skills,
        job_skills
    )


    # --------------------------------------------------------
    # Keyword matching
    # --------------------------------------------------------

    keyword_score, matching_keywords, missing_keywords = (
        calculate_keyword_score(
            resume_text,
            job_description
        )
    )


    # --------------------------------------------------------
    # Detect resume sections
    # --------------------------------------------------------

    sections = detect_sections(
        resume_text
    )


    # --------------------------------------------------------
    # Calculate section score
    # --------------------------------------------------------

    important_sections = [
        "contact",
        "summary",
        "skills",
        "education",
        "experience",
        "projects"
    ]

    detected_count = 0

    for section in important_sections:

        if sections.get(section):

            detected_count += 1


    section_score = round(
        (detected_count / len(important_sections))
        * 100
    )


    # --------------------------------------------------------
    # Final ATS score
    # --------------------------------------------------------

    ats_score = calculate_ats_score(
        skill_score,
        section_score,
        keyword_score
    )


    # --------------------------------------------------------
    # Return analysis
    # --------------------------------------------------------

    return {

        "filename": file.filename,

        "ats_score": ats_score,

        "skill_score": skill_score,

        "section_score": section_score,

        "keyword_score": keyword_score,

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "matching_keywords": matching_keywords,

        "missing_keywords": missing_keywords,

        "sections": sections
    }