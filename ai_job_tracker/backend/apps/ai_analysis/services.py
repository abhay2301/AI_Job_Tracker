import os
import json
from pydantic import BaseModel
from google import genai
from google.genai import types

class JobAnalysisResponse(BaseModel):
    match_score: int
    matching_keywords: str
    missing_keywords: str
    recommendations: str

def analyze_job_and_resume(job_description, resume_text):
    """
    Service to perform AI analysis of a job description against a resume using Google Gemini API.
    """
    job_desc = job_description or ""
    res_text = resume_text or ""
    
    if not job_desc or not res_text:
        return {
            "match_score": 0,
            "matching_keywords": "None",
            "missing_keywords": "None",
            "recommendations": "Analysis failed or missing inputs."
        }
        
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "match_score": 0,
            "matching_keywords": "None",
            "missing_keywords": "None",
            "recommendations": "GEMINI_API_KEY is not configured in the environment."
        }
        
    try:
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert technical recruiter and ATS (Applicant Tracking System).
        Analyze the following resume against the provided job description.
        
        Job Description:
        {job_desc}
        
        Resume:
        {res_text}
        
        Provide your analysis in the exact JSON structure requested:
        - match_score: An integer from 0 to 100 representing how well the resume fits the job description.
        - matching_keywords: A comma-separated string of key skills and qualifications found in both the job description and resume.
        - missing_keywords: A comma-separated string of key skills and qualifications present in the job description but missing from the resume.
        - recommendations: A short string with actionable advice on how the candidate can improve their resume for this job.
        """
        
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JobAnalysisResponse,
            ),
        )
        
        result = json.loads(response.text)
        return {
            "match_score": result.get("match_score", 0),
            "matching_keywords": result.get("matching_keywords", "None"),
            "missing_keywords": result.get("missing_keywords", "None"),
            "recommendations": result.get("recommendations", "No recommendations available.")
        }
    except Exception as e:
        print(f"Error during AI analysis: {e}")
        return {
            "match_score": 0,
            "matching_keywords": "None",
            "missing_keywords": "None",
            "recommendations": f"Error during AI analysis: {str(e)}"
        }
