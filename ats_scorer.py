# ============================================================
# SMART RESUME ANALYZER - ATS SCORER
# ============================================================


def calculate_ats_score(
    skill_score,
    section_score,
    keyword_score
):
    """
    Calculate the overall ATS score.

    Weight:
        Skills   = 50%
        Structure = 25%
        Keywords = 25%
    """

    # Make sure scores stay between 0 and 100
    skill_score = max(0, min(100, skill_score))
    section_score = max(0, min(100, section_score))
    keyword_score = max(0, min(100, keyword_score))

    final_score = (
        skill_score * 0.50
        + section_score * 0.25
        + keyword_score * 0.25
    )

    return round(final_score)