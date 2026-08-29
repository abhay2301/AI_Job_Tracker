from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.jobs.models import JobApplication
from apps.resumes.models import Resume
from .models import JobAnalysis
from .services import analyze_job_and_resume

@login_required
def analyze_job_view(request, job_id):
    job = get_object_or_404(JobApplication, id=job_id, user=request.user)
    
    if request.method == "POST":
        resume_id = request.POST.get("resume_id")
        if not resume_id:
            messages.error(request, "Please select a resume for analysis.")
            return redirect("jobs:detail", pk=job_id)
            
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        
        # Run the mock analysis service
        result = analyze_job_and_resume(job.job_description, resume.extracted_text)
        
        # Save or update the analysis record
        analysis, created = JobAnalysis.objects.update_or_create(
            job=job,
            defaults={
                "resume": resume,
                "match_score": result["match_score"],
                "matching_keywords": result["matching_keywords"],
                "missing_keywords": result["missing_keywords"],
                "recommendations": result["recommendations"],
            }
        )
        
        messages.success(request, "AI Analysis completed successfully!")
        return redirect("jobs:detail", pk=job_id)
        
    # If not POST, just redirect back
    return redirect("jobs:detail", pk=job_id)
