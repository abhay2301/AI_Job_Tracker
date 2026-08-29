from django import forms

from .models import Resume


class ResumeUploadForm(forms.ModelForm):

    class Meta:
        model = Resume

        fields = (
            "title",
            "file",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Python Developer Resume",
                }
            ),

            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf",
                }
            ),
        }

    def clean_file(self):
        file = self.cleaned_data["file"]

        # Maximum file size: 5 MB
        max_size = 5 * 1024 * 1024

        if file.size > max_size:
            raise forms.ValidationError(
                "Resume file size cannot exceed 5 MB."
            )

        # Validate extension
        if not file.name.lower().endswith(".pdf"):
            raise forms.ValidationError(
                "Only PDF files are allowed."
            )

        return file