from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = (
            "company",
            "position",
            "job_url",
            "status",
            "application_date",
            "job_description",
        )

        widgets = {
            "company": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Google",
                }
            ),

            "position": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Software Engineer Intern",
                }
            ),

            "job_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://...",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "application_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "job_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Paste the job description here...",
                }
            ),
        }