"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from apps.jobs.views import dashboard
from apps.users.views import login_view, verify_otp_view


urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        dashboard,
        name="dashboard",
    ),

    path(
        "users/",
        include("apps.users.urls"),
    ),

    path(
        "jobs/",
        include("apps.jobs.urls"),
    ),

    path(
        "resumes/",
        include("apps.resumes.urls"),
    ),

    path(
        "ai/",
        include("apps.ai_analysis.urls"),
    ),

    path(
        "login/",
        login_view,
        name="login",
    ),

    path(
        "verify-otp/",
        verify_otp_view,
        name="verify_otp",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )