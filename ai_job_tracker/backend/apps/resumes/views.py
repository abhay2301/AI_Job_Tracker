import pymupdf

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ResumeUploadForm
from .models import Resume


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "resumes/resume_list.html",
        {
            "resumes": resumes,
        },
    )


@login_required
def resume_upload(request):

    if request.method == "POST":

        form = ResumeUploadForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            resume = form.save(
                commit=False
            )

            resume.user = request.user

            # Extract PDF text
            try:
                file_data = resume.file.read()
                with pymupdf.open(stream=file_data, filetype="pdf") as pdf:

                    text = ""

                    for page in pdf:
                        text += page.get_text()

                resume.extracted_text = text
                
                # Reset file pointer so Django saves the file correctly
                resume.file.seek(0)

                resume.save()

                messages.success(
                    request,
                    "Resume uploaded successfully."
                )

                return redirect(
                    "resumes:detail",
                    pk=resume.pk,
                )

            except Exception as e:
                messages.error(
                    request,
                    "Unable to process the PDF."
                )

    else:
        form = ResumeUploadForm()

    return render(
        request,
        "resumes/resume_form.html",
        {
            "form": form,
        },
    )


import re

@login_required
def resume_detail(request, pk):

    resume = get_object_or_404(
        Resume,
        pk=pk,
        user=request.user,
    )
    
    # Format text for display without needing custom template tags
    text = resume.extracted_text or ""
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(' • ', '<br>&bull; ')
    text = text.replace(' - ', '<br>&bull; ')
    
    headers = [
        "Experience", "Professional Summary", "Education", "Skills", 
        "Projects", "Certifications", "Languages", "Summary", 
        "Technical Skills", "Work Experience"
    ]
    
    for header in headers:
        pattern = re.compile(rf'\b({header})\b', re.IGNORECASE)
        text = pattern.sub(r'</p><h5 class="fw-bold text-primary mt-4 mb-2">\1</h5><p>', text)
        
    formatted_text = f"<p>{text}</p>".replace("<p></p>", "").replace("<p> </p>", "")

    return render(
        request,
        "resumes/resume_detail.html",
        {
            "resume": resume,
            "formatted_text": formatted_text,
        },
    )


@login_required
def resume_download(request, pk):

    resume = get_object_or_404(
        Resume,
        pk=pk,
        user=request.user,
    )

    return FileResponse(
        resume.file.open("rb"),
        as_attachment=True,
        filename=resume.file.name.split("/")[-1],
    )


@login_required
def resume_delete(request, pk):

    resume = get_object_or_404(
        Resume,
        pk=pk,
        user=request.user,
    )

    if request.method == "POST":

        resume.file.delete(
            save=False
        )

        resume.delete()

        messages.success(
            request,
            "Resume deleted successfully."
        )

        return redirect(
            "resumes:list"
        )

    return render(
        request,
        "resumes/resume_detail.html",
        {
            "resume": resume,
            "confirm_delete": True,
        },
    )