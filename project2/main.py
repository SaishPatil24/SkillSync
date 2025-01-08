from fastapi import FastAPI, UploadFile, Form
from typing import List
from scraper import scrape_jobs
from skills import extract_job_skills, parse_resume, skill_gap

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the AI-Powered Career Navigator"}

@app.post("/scrape_jobs/")
async def fetch_jobs(job_title: str = Form(...), location: str = Form(...)):
    jobs = scrape_jobs(job_title, location)
    return {"jobs": jobs}

@app.post("/analyze_resume/")
async def analyze_resume(resume: UploadFile, job_title: str, location: str):
    # Parse resume for skills
    resume_text = await resume.read()
    resume_skills = parse_resume(resume_text)
    
    # Scrape job listings
    jobs = scrape_jobs(job_title, location)
    job_descriptions = [job["Summary"] for job in jobs if "Summary" in job]
    
    # Extract skills from job descriptions
    job_skills = extract_job_skills(job_descriptions)
    
    # Skill gap analysis
    missing_skills = skill_gap(job_skills, resume_skills)
    
    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "missing_skills": missing_skills,
    }