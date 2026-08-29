from django.urls import path
from . import views

app_name = "ai_analysis"

urlpatterns = [
    path("analyze/job/<int:job_id>/", views.analyze_job_view, name="analyze_job"),
]
