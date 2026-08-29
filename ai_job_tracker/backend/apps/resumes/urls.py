from django.urls import path

from . import views


app_name = "resumes"


urlpatterns = [
    path(
        "",
        views.resume_list,
        name="list",
    ),

    path(
        "upload/",
        views.resume_upload,
        name="upload",
    ),

    path(
        "<int:pk>/",
        views.resume_detail,
        name="detail",
    ),

    path(
        "<int:pk>/download/",
        views.resume_download,
        name="download",
    ),

    path(
        "<int:pk>/delete/",
        views.resume_delete,
        name="delete",
    ),
]