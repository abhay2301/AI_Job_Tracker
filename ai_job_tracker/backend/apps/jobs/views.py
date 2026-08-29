from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobApplicationForm
from .models import JobApplication


@login_required
def dashboard(request):
    applications = JobApplication.objects.filter(
        user=request.user
    )

    applied_count = applications.filter(
        status=JobApplication.Status.APPLIED
    ).count()

    interview_count = applications.filter(
        status=JobApplication.Status.INTERVIEW
    ).count()

    selected_count = applications.filter(
        status=JobApplication.Status.SELECTED
    ).count()

    other_count = applications.exclude(
        status__in=[
            JobApplication.Status.APPLIED,
            JobApplication.Status.INTERVIEW,
            JobApplication.Status.SELECTED,
        ]
    ).count()

    context = {
        "total_applications": applications.count(),
        "applied_count": applied_count,
        "interview_count": interview_count,
        "selected_count": selected_count,
        "recent_applications": applications.order_by(
            "-created_at"
        )[:5],
    }
    
    total = applied_count + interview_count + selected_count + other_count
    context.update({
        'applied_percent': round((applied_count / total) * 100) if total else 0,
        'interview_percent': round((interview_count / total) * 100) if total else 0,
        'selected_percent': round((selected_count / total) * 100) if total else 0,
        'other_percent': round((other_count / total) * 100) if total else 0,
        'other_count': other_count,  # e.g., rejected, withdrawn, etc.
    })

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )


@login_required
def job_list(request):
    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "jobs/job_list.html",
        {
            "applications": applications,
        },
    )


@login_required
def job_create(request):

    if request.method == "POST":
        form = JobApplicationForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)

            job.user = request.user

            job.save()

            messages.success(
                request,
                "Job application added successfully."
            )

            return redirect("jobs:list")

    else:
        form = JobApplicationForm()

    return render(
        request,
        "jobs/job_form.html",
        {
            "form": form,
        },
    )


from apps.resumes.models import Resume

@login_required
def job_detail(request, pk):

    job = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    resumes = Resume.objects.filter(user=request.user)
    
    ai_analysis = getattr(job, 'ai_analysis', None)

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "resumes": resumes,
            "ai_analysis": ai_analysis,
        },
    )


@login_required
def job_edit(request, pk):

    job = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST,
            instance=job,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Job application updated successfully."
            )

            return redirect(
                "jobs:detail",
                pk=job.pk,
            )

    else:

        form = JobApplicationForm(
            instance=job,
        )

    return render(
        request,
        "jobs/job_form.html",
        {
            "form": form,
            "object": job,
        },
    )


@login_required
def job_delete(request, pk):

    job = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        job.delete()

        messages.success(
            request,
            "Job application deleted successfully."
        )

        return redirect("jobs:list")

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "confirm_delete": True,
        },
    )