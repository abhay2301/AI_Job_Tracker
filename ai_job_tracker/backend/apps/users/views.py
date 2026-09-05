from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import LoginForm, OTPForm, RegisterForm
from .models import UserOTP


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your account has been created successfully. Please log in with OTP verification."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user_model = get_user_model()
            try:
                if "@" in username_or_email:
                    user_obj = user_model.objects.get(email__iexact=username_or_email)
                else:
                    user_obj = user_model.objects.get(username__iexact=username_or_email)
            except user_model.DoesNotExist:
                user_obj = None

            if user_obj:
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password,
                )
            else:
                user = None

            if user is None:
                messages.error(request, "Invalid username or password.")
            else:
                request.session["pending_user_id"] = user.pk
                otp = UserOTP.generate_for_user(user)

                try:
                    send_mail(
                        subject="Your AI Job Tracker login code",
                        message=(
                            f"Your one-time password is {otp.otp_code}. "
                            "It expires in 1 minute."
                        ),
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@ai-job-tracker.local"),
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                except Exception:
                    messages.warning(
                        request,
                        "OTP email could not be sent, but the code was generated for testing."
                    )

                messages.success(
                    request,
                    "A one-time password has been sent to your email."
                )
                return redirect("verify_otp")

    else:
        form = LoginForm()

    return render(
        request,
        "registration/login.html",
        {"form": form},
    )


def verify_otp_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    pending_user_id = request.session.get("pending_user_id")

    if not pending_user_id:
        return redirect("login")

    user = get_user_model().objects.filter(pk=pending_user_id).first()

    if user is None:
        request.session.pop("pending_user_id", None)
        return redirect("login")

    has_valid_otp = user.otps.filter(
        used_at__isnull=True,
        expires_at__gt=timezone.now()
    ).exists()

    if not has_valid_otp:
        request.session.pop("pending_user_id", None)
        request.session.pop("otp_failed_attempts", None)
        messages.error(request, "Your login session expired. Please try again.")
        return redirect("login")

    if request.method == "POST":
        # Rate limiting: Max 3 failed attempts
        failed_attempts = request.session.get("otp_failed_attempts", 0)
        if failed_attempts >= 3:
            messages.error(request, "Too many failed attempts. Please login again.")
            request.session.pop("pending_user_id", None)
            request.session.pop("otp_failed_attempts", None)
            return redirect("login")

        form = OTPForm(request.POST)

        if form.is_valid():
            otp = user.otps.filter(
                used_at__isnull=True,
                expires_at__gt=timezone.now(),
            ).order_by("-created_at").first()

            if otp and otp.is_valid(form.cleaned_data["otp_code"]):
                otp.used_at = timezone.now()
                otp.save(update_fields=["used_at"])

                login(request, user)
                request.session.pop("pending_user_id", None)
                request.session.pop("otp_failed_attempts", None)

                messages.success(request, "OTP verified successfully. You are now logged in.")
                return redirect("dashboard")

            request.session["otp_failed_attempts"] = failed_attempts + 1
            messages.error(request, "invalid or expired OTP code.")
    else:
        form = OTPForm()

    return render(
        request,
        "registration/verify_otp.html",
        {"form": form, "pending_user": user},
    )