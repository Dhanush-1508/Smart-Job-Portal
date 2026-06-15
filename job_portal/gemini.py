from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def get_ai_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    jobs = [
        line.strip()
        for line in response.text.split("\n")
        if line.strip()
    ]

    return jobs


def get_ats_score(resume_text):
    if not resume_text:
        return 0

    prompt = f"""
    Give only one number from 0 to 100 for ATS score of this resume.
    No text, only number.

    Resume:
    {resume_text[:5000]}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if not response or not response.text:
            return 0

        return int(''.join(filter(str.isdigit, response.text))[:3])
    except:
        return 0