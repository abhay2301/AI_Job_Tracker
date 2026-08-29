from django.db import models

class JobAnalysis(models.Model):
    job = models.OneToOneField(
        "jobs.JobApplication",
        on_delete=models.CASCADE,
        related_name="ai_analysis",
    )
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="ai_analyses",
    )
    match_score = models.IntegerField(default=0)
    matching_keywords = models.TextField(blank=True)
    missing_keywords = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.job.position} at {self.job.company}"
