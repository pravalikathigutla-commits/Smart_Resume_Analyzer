from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

import io

from module.resume_parser import extract_resume_text
from module.skill_extractor import extract_skills
from module.keyword_matcher import calculate_keyword_score
from module.resume_matcher import calculate_match
from module.resume_sections import (
    detect_sections,
    calculate_section_score
)
from module.ats_scorer import calculate_ats_score


app = FastAPI(
    title="Smart Resume Analyzer",
    description="AI-powered ATS Resume Analyzer",
    version="1.0.0"
)

ELIGIBILITY_THRESHOLD = 70


# ============================================================
# ELIGIBILITY THRESHOLD
# ============================================================

ELIGIBILITY_THRESHOLD = 70


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Smart Resume Analyzer</title>


<style>

/* ============================================================
   GLOBAL
   ============================================================ */

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #f8fafc
        );

    color: #1e293b;
}


.container {

    width: 92%;

    max-width: 1100px;

    margin: 40px auto;

}


/* ============================================================
   HEADER
   ============================================================ */

.header {

    text-align: center;

    margin-bottom: 30px;

}


.header h1 {

    font-size: 38px;

    margin-bottom: 10px;

    color: #1e3a8a;

}


.header p {

    color: #64748b;

    font-size: 17px;

}


/* ============================================================
   CARD
   ============================================================ */

.card {

    background: white;

    padding: 30px;

    border-radius: 18px;

    box-shadow:
        0 10px 30px
        rgba(15, 23, 42, 0.08);

    margin-bottom: 25px;

}


/* ============================================================
   FORM
   ============================================================ */

label {

    display: block;

    font-weight: bold;

    margin-bottom: 8px;

}


input[type="file"],
textarea {

    width: 100%;

    padding: 14px;

    border: 1px solid #cbd5e1;

    border-radius: 10px;

    margin-bottom: 20px;

    font-size: 15px;

}


textarea {

    min-height: 200px;

    resize: vertical;

}


button {

    width: 100%;

    padding: 15px;

    border: none;

    border-radius: 10px;

    background: #2563eb;

    color: white;

    font-size: 17px;

    font-weight: bold;

    cursor: pointer;

}


button:hover {

    background: #1d4ed8;

}


/* ============================================================
   LOADING
   ============================================================ */

.loading {

    text-align: center;

    font-size: 18px;

    padding: 25px;

}


/* ============================================================
   SCORE CONTAINER
   ============================================================ */

.score-container {

    text-align: center;

    margin: 20px 0 30px;

}


.score-circle {

    width: 190px;

    height: 190px;

    border-radius: 50%;

    margin: auto;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    color: white;

    box-shadow:
        0 10px 25px
        rgba(37, 99, 235, 0.3);

}


.score-circle.eligible {

    background:
        linear-gradient(
            135deg,
            #16a34a,
            #22c55e
        );

}


.score-circle.not-eligible {

    background:
        linear-gradient(
            135deg,
            #dc2626,
            #ef4444
        );

}


.score-number {

    font-size: 52px;

    font-weight: bold;

}


.score-label {

    font-size: 15px;

}


/* ============================================================
   ELIGIBILITY
   ============================================================ */

.eligibility {

    text-align: center;

    padding: 18px;

    border-radius: 12px;

    margin: 20px 0;

    font-size: 22px;

    font-weight: bold;

}


.eligibility.eligible {

    background: #dcfce7;

    color: #166534;

    border: 1px solid #86efac;

}


.eligibility.not-eligible {

    background: #fee2e2;

    color: #991b1b;

    border: 1px solid #fca5a5;

}


.threshold {

    text-align: center;

    color: #64748b;

    margin-bottom: 25px;

}


/* ============================================================
   SCORE GRID
   ============================================================ */

.score-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 20px;

}


.score-card {

    padding: 22px;

    border-radius: 14px;

    text-align: center;

    background: #f8fafc;

    border: 1px solid #e2e8f0;

}


.score-card h3 {

    margin: 0 0 10px;

}


.score-value {

    font-size: 32px;

    font-weight: bold;

    color: #2563eb;

}


/* ============================================================
   TWO COLUMN
   ============================================================ */

.two-column {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 20px;

}


/* ============================================================
   TAGS
   ============================================================ */

.tag-container {

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

}


.tag {

    padding: 8px 12px;

    border-radius: 20px;

    font-size: 14px;

    background: #e0e7ff;

    color: #3730a3;

}


.match {

    background: #dcfce7;

    color: #166534;

}


.missing {

    background: #fee2e2;

    color: #991b1b;

}


.empty-message {

    color: #64748b;

    font-style: italic;

}


/* ============================================================
   SECTION LIST
   ============================================================ */

.section-list {

    list-style: none;

    padding: 0;

}


.section-list li {

    padding: 12px;

    margin-bottom: 8px;

    border-radius: 8px;

}


.section-found {

    background: #dcfce7;

    color: #166534;

}


.section-missing {

    background: #fee2e2;

    color: #991b1b;

}


/* ============================================================
   RECOMMENDATIONS
   ============================================================ */

.recommendation {

    padding: 14px;

    margin-bottom: 10px;

    border-left: 5px solid #2563eb;

    background: #eff6ff;

    border-radius: 6px;

}


/* ============================================================
   JOB INFO
   ============================================================ */

.job-info {

    background: #f8fafc;

    padding: 18px;

    border-radius: 12px;

    margin-bottom: 20px;

}


.job-info strong {

    color: #1e3a8a;

}


/* ============================================================
   ERROR
   ============================================================ */

.error {

    background: #fee2e2;

    color: #991b1b;

    padding: 18px;

    border-radius: 10px;

    border: 1px solid #fca5a5;

}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 700px) {

    .score-grid,
    .two-column {

        grid-template-columns: 1fr;

    }


    .header h1 {

        font-size: 28px;

    }


    .card {

        padding: 20px;

    }


    .score-circle {

        width: 160px;

        height: 160px;

    }


    .score-number {

        font-size: 44px;

    }

}

</style>

</head>


<body>


<div class="container">


    <!-- ======================================================
         HEADER
         ====================================================== -->

    <div class="header">

        <h1>
            🚀 Smart Resume Analyzer
        </h1>

        <p>
            Analyze your resume against a job description
            and check your ATS eligibility.
        </p>

    </div>


    <!-- ======================================================
         UPLOAD FORM
         ====================================================== -->

    <div class="card">

        <form id="resumeForm">


            <label>
                📄 Upload Resume
            </label>


            <input
                type="file"
                id="resume"
                accept=".pdf,.docx"
                required
            >


            <label>
                💼 Job Description
            </label>


            <textarea
                id="job_description"
                placeholder="Paste the complete job description here..."
                required
            ></textarea>


            <button type="submit">

                🚀 Analyze Resume

            </button>


        </form>

    </div>


    <!-- ======================================================
         RESULTS
         ====================================================== -->

    <div id="result"></div>


</div>


<script>


// ============================================================
// CREATE TAGS
// ============================================================

function createTags(items, className = "") {

    if (!items || items.length === 0) {

        return `
            <p class="empty-message">
                None found
            </p>
        `;

    }


    return items.map(
        item => `
            <span class="tag ${className}">
                ${escapeHTML(item)}
            </span>
        `
    ).join("");

}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        String(value);

    return div.innerHTML;

}


// ============================================================
// DISPLAY RESULTS
// ============================================================

function displayResults(data) {


    const eligible =
        data.eligible;


    const statusClass =
        eligible
            ? "eligible"
            : "not-eligible";


    const statusText =
        eligible
            ? "✅ ELIGIBLE FOR THIS JOB"
            : "❌ NOT ELIGIBLE FOR THIS JOB";


    // --------------------------------------------------------
    // Section HTML
    // --------------------------------------------------------

    let sectionHTML = "";


    const sectionNames = {

        contact: "Contact",

        summary: "Professional Summary",

        skills: "Skills",

        education: "Education",

        experience: "Experience",

        projects: "Projects",

        certifications: "Certifications",

        achievements: "Achievements",

        coding_profiles: "Coding Profiles"

    };


    Object.entries(sectionNames)
        .forEach(
            ([key, name]) => {


                const content =
                    data.sections[key] || [];


                const found =
                    content.length > 0;


                sectionHTML += `

                    <li class="${
                        found
                            ? "section-found"
                            : "section-missing"
                    }">

                        ${
                            found
                                ? "✅"
                                : "❌"
                        }

                        <strong>
                            ${name}
                        </strong>

                        ${
                            found
                                ? " - Found"
                                : " - Not Found"
                        }

                    </li>

                `;

            }
        );


    // --------------------------------------------------------
    // Recommendations
    // --------------------------------------------------------

    let recommendations = [];


    if (data.missing_skills &&
        data.missing_skills.length > 0) {

        recommendations.push(
            "Add relevant missing job skills to your resume if you genuinely have those skills."
        );

    }


    if (data.missing_keywords &&
        data.missing_keywords.length > 0) {

        recommendations.push(
            "Consider naturally including important keywords from the job description."
        );

    }


    if (data.section_score < 100) {

        recommendations.push(
            "Improve your resume structure by adding the missing recommended sections."
        );

    }


    if (data.skill_score < 70) {

        recommendations.push(
            "Increase alignment between your resume skills and the job requirements."
        );

    }


    if (data.keyword_score < 70) {

        recommendations.push(
            "Improve keyword alignment with the job description."
        );

    }


    if (eligible) {

        recommendations.push(
            "Your resume currently meets the 70% eligibility threshold for this job."
        );

    }
    else {

        recommendations.push(
            "Your ATS score is below 70%. Improve the areas above and analyze the resume again."
        );

    }


    let recommendationHTML = "";


    recommendations.forEach(
        recommendation => {

            recommendationHTML += `

                <div class="recommendation">

                    💡 ${escapeHTML(
                        recommendation
                    )}

                </div>

            `;

        }
    );


    // --------------------------------------------------------
    // Main result HTML
    // --------------------------------------------------------

    document
        .getElementById("result")
        .innerHTML = `


        <!-- ==================================================
             STATUS
             ================================================== -->

        <div class="card">


            <div class="score-container">

                <div class="score-circle ${statusClass}">

                    <div class="score-number">

                        ${data.ats_score}%

                    </div>

                    <div class="score-label">

                        ATS SCORE

                    </div>

                </div>

            </div>


            <div class="eligibility ${statusClass}">

                ${statusText}

            </div>


            <div class="threshold">

                Eligibility threshold:
                <strong>70%</strong>

            </div>


            ${
                eligible

                    ? `
                        <p style="
                            text-align:center;
                            color:#166534;
                            font-weight:bold;
                        ">

                            Your resume meets the minimum
                            ATS score required for this job.

                        </p>
                    `

                    : `
                        <p style="
                            text-align:center;
                            color:#991b1b;
                            font-weight:bold;
                        ">

                            Your resume needs to reach
                            at least 70% to be eligible.

                        </p>
                    `
            }


        </div>


        <!-- ==================================================
             SCORE BREAKDOWN
             ================================================== -->

        <div class="card">

            <h2>
                📊 Score Breakdown
            </h2>


            <div class="score-grid">


                <div class="score-card">

                    <h3>
                        🧠 Skills
                    </h3>

                    <div class="score-value">

                        ${data.skill_score}%

                    </div>

                </div>


                <div class="score-card">

                    <h3>
                        🔑 Keywords
                    </h3>

                    <div class="score-value">

                        ${data.keyword_score}%

                    </div>

                </div>


                <div class="score-card">

                    <h3>
                        📑 Structure
                    </h3>

                    <div class="score-value">

                        ${data.section_score}%

                    </div>

                </div>


            </div>

        </div>


        <!-- ==================================================
             RESUME INFORMATION
             ================================================== -->

        <div class="card">

            <h2>
                📄 Resume Information
            </h2>

            <div class="job-info">

                <strong>File:</strong>

                ${escapeHTML(
                    data.filename
                )}

            </div>

        </div>


        <!-- ==================================================
             RESUME SKILLS
             ================================================== -->

        <div class="card">

            <h2>
                🛠️ Resume Skills
            </h2>


            <div class="tag-container">

                ${createTags(
                    data.resume_skills
                )}

            </div>

        </div>


        <!-- ==================================================
             JOB SKILLS
             ================================================== -->

        <div class="card">

            <h2>
                💼 Job Description Skills
            </h2>


            <div class="tag-container">

                ${createTags(
                    data.job_skills
                )}

            </div>

        </div>


        <!-- ==================================================
             MATCHING / MISSING SKILLS
             ================================================== -->

        <div class="two-column">


            <div class="card">

                <h2>
                    ✅ Matching Skills
                </h2>


                <div class="tag-container">

                    ${createTags(
                        data.matching_skills,
                        "match"
                    )}

                </div>

            </div>


            <div class="card">

                <h2>
                    ❌ Missing Skills
                </h2>


                <div class="tag-container">

                    ${createTags(
                        data.missing_skills,
                        "missing"
                    )}

                </div>

            </div>


        </div>


        <!-- ==================================================
             KEYWORDS
             ================================================== -->

        <div class="two-column">


            <div class="card">

                <h2>
                    ✅ Matching Keywords
                </h2>


                <div class="tag-container">

                    ${createTags(
                        data.matching_keywords,
                        "match"
                    )}

                </div>

            </div>


            <div class="card">

                <h2>
                    ❌ Missing Keywords
                </h2>


                <div class="tag-container">

                    ${createTags(
                        data.missing_keywords,
                        "missing"
                    )}

                </div>

            </div>


        </div>


        <!-- ==================================================
             RESUME SECTIONS
             ================================================== -->

        <div class="card">

            <h2>
                📑 Resume Sections
            </h2>


            <ul class="section-list">

                ${sectionHTML}

            </ul>


            <p class="empty-message">

                Professional Summary and Achievements
                are optional and do not reduce the section score.

            </p>

        </div>


        <!-- ==================================================
             RECOMMENDATIONS
             ================================================== -->

        <div class="card">

            <h2>
                💡 Recommendations
            </h2>


            ${recommendationHTML}

        </div>


    `;

}


// ============================================================
// FORM SUBMISSION
// ============================================================

document
    .getElementById("resumeForm")
    .addEventListener(
        "submit",
        async function(event) {


            event.preventDefault();


            const file =
                document
                    .getElementById("resume")
                    .files[0];


            const jobDescription =
                document
                    .getElementById("job_description")
                    .value
                    .trim();


            // ------------------------------------------------
            // Validate file
            // ------------------------------------------------

            if (!file) {

                document
                    .getElementById("result")
                    .innerHTML = `

                        <div class="card">

                            <div class="error">

                                ❌ Please select a resume file.

                            </div>

                        </div>

                    `;

                return;

            }


            // ------------------------------------------------
            // Validate job description
            // ------------------------------------------------

            if (!jobDescription) {

                document
                    .getElementById("result")
                    .innerHTML = `

                        <div class="card">

                            <div class="error">

                                ❌ Please enter the job description.

                            </div>

                        </div>

                    `;

                return;

            }


            // ------------------------------------------------
            // FormData
            // ------------------------------------------------

            const formData =
                new FormData();


            formData.append(
                "file",
                file
            );


            formData.append(
                "job_description",
                jobDescription
            );


            // ------------------------------------------------
            // Loading
            // ------------------------------------------------

            document
                .getElementById("result")
                .innerHTML = `

                    <div class="card loading">

                        ⏳ Analyzing your resume...

                        <br><br>

                        Extracting skills,
                        keywords and resume sections.

                    </div>

                `;


            try {


                // ------------------------------------------------
                // API request
                // ------------------------------------------------

                const response =
                    await fetch(
                        "/analyze",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Analysis failed."
                    );

                }


                if (data.error) {

                    throw new Error(
                        data.error
                    );

                }


                // ------------------------------------------------
                // Display results
                // ------------------------------------------------

                displayResults(data);


            }

            catch(error) {


                document
                    .getElementById("result")
                    .innerHTML = `

                        <div class="card">

                            <div class="error">

                                ❌ ${escapeHTML(
                                    error.message
                                )}

                            </div>

                        </div>

                    `;

            }

        }
    );


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

    # ========================================================
    # VALIDATE FILE
    # ========================================================

    if not file.filename:
        return {
            "error": "Please select a resume file."
        }

    filename = file.filename.lower()

    # ========================================================
    # VALIDATE FILE TYPE
    # ========================================================

    if not (
        filename.endswith(".pdf")
        or filename.endswith(".docx")
    ):
        return {
            "error": "Unsupported file type. Please upload PDF or DOCX."
        }

    # ========================================================
    # VALIDATE JOB DESCRIPTION
    # ========================================================

    if not job_description.strip():
        return {
            "error": "Please provide a job description."
        }

    # ========================================================
    # READ FILE
    # ========================================================

    try:
        contents = await file.read()
    except Exception as error:
        return {
            "error": f"Could not read uploaded file: {str(error)}"
        }

    if not contents:
        return {
            "error": "The uploaded resume is empty."
        }

    # ========================================================
    # CREATE FILE OBJECT
    # ========================================================

    file_object = io.BytesIO(contents)

    # ========================================================
    # EXTRACT RESUME TEXT
    # ========================================================

    try:
        resume_text = extract_resume_text(
            file_object,
            file.filename
        )

    except Exception as error:
        return {
            "error": f"Could not read resume: {str(error)}"
        }

    if not resume_text or not resume_text.strip():
        return {
            "error": "Could not extract text from the resume."
        }

    # ========================================================
    # EXTRACT RESUME SKILLS
    # ========================================================

    try:
        resume_skills = extract_skills(
            resume_text
        )

    except Exception as error:
        return {
            "error": f"Could not extract resume skills: {str(error)}"
        }

    # ========================================================
    # EXTRACT JOB SKILLS
    # ========================================================

    try:
        job_skills = extract_skills(
            job_description
        )

    except Exception as error:
        return {
            "error": f"Could not extract job skills: {str(error)}"
        }

    # ========================================================
    # MATCH RESUME SKILLS WITH JOB SKILLS
    # ========================================================

    try:
        (
            skill_score,
            matching_skills,
            missing_skills
        ) = calculate_match(
            resume_skills,
            job_skills
        )

    except Exception as error:
        return {
            "error": f"Skill matching failed: {str(error)}"
        }

    # ========================================================
    # KEYWORD ANALYSIS
    # ========================================================

    try:
        (
            keyword_score,
            matching_keywords,
            missing_keywords
        ) = calculate_keyword_score(
            resume_text,
            job_description
        )

    except Exception as error:
        return {
            "error": f"Keyword analysis failed: {str(error)}"
        }

    # ========================================================
    # DETECT RESUME SECTIONS
    # ========================================================

    try:
        sections = detect_sections(
            resume_text
        )

    except Exception as error:
        return {
            "error": f"Resume section detection failed: {str(error)}"
        }

    # ========================================================
    # CALCULATE SECTION SCORE
    # ========================================================

    try:
        section_score = calculate_section_score(
            sections
        )

    except Exception as error:
        return {
            "error": f"Section score calculation failed: {str(error)}"
        }

    # ========================================================
    # FINAL ATS SCORE
    # ========================================================

    try:
        ats_score = calculate_ats_score(
            skill_score,
            section_score,
            keyword_score
        )

    except Exception as error:
        return {
            "error": f"ATS score calculation failed: {str(error)}"
        }

    # ========================================================
    # ELIGIBILITY
    # ========================================================

    eligible = ats_score >= ELIGIBILITY_THRESHOLD

    if eligible:
        eligibility_status = "ELIGIBLE"
    else:
        eligibility_status = "NOT ELIGIBLE"

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {
        "filename": file.filename,

        "ats_score": ats_score,

        "eligibility_threshold": ELIGIBILITY_THRESHOLD,

        "eligible": eligible,

        "eligibility_status": eligibility_status,

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