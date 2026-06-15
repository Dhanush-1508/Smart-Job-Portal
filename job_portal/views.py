from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Job, Resume, Application
from .gemini import get_ai_response, get_ats_score
from .resume_utils import extract_resume_text


# =========================
# AUTH PAGE (LOGIN + SIGNUP)
# =========================
def auth_page(request):

    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            fullname = request.POST.get("fullname", "").strip()
            email = request.POST.get("email", "").strip().lower()
            password = request.POST.get("password", "")
            confirm_password = request.POST.get("confirm_password", "")

            if not fullname or not email or not password:
                return render(request, "auth.html", {
                    "error": "Please fill in all required fields.",
                    "active_tab": "signup",
                })

            if password != confirm_password:
                return render(request, "auth.html", {
                    "error": "Passwords do not match.",
                    "active_tab": "signup",
                })

            if User.objects.filter(username=email).exists():
                return render(request, "auth.html", {
                    "error": "An account with this email already exists.",
                    "active_tab": "signup",
                })

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=fullname,
            )
            user.save()

            login(request, user)
            return redirect("index")

        elif action == "login":
            username = request.POST.get("username", "").strip().lower()
            password = request.POST.get("password", "")

            if not username or not password:
                return render(request, "auth.html", {
                    "error": "Please enter email and password.",
                    "active_tab": "login",
                })

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return render(request, "auth.html", {
                    "error": "Invalid email or password.",
                    "active_tab": "login",
                })

    return render(request, "auth.html", {
        "active_tab": "login",
    })


# =========================
# LOGOUT
# =========================
def logout_page(request):
    logout(request)
    return redirect("auth")


# =========================
# HOME PAGE (PROTECTED)
# =========================
@login_required(login_url='auth')
def index(request):

    if request.method == "POST":
        if request.FILES.get("resume"):
            Resume.objects.all().delete()

            resume_obj = Resume.objects.create(
                resume=request.FILES["resume"]
            )

            text = extract_resume_text(resume_obj.resume.path) or ""
            resume_obj.ats_score = get_ats_score(text)
            resume_obj.save()

            return redirect("index")

    resumes = Resume.objects.all()

    return render(request, "index.html", {
        "resumes": resumes
    })


# =========================
# JOB LIST + ADD JOB
# =========================
@login_required(login_url='auth')
def jobs(request):

    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("company")
        location = request.POST.get("location")
        salary = request.POST.get("salary")
        job_type = request.POST.get("job_type")
        description = request.POST.get("description")

        if title and company and location and salary and job_type:
            Job.objects.create(
                title=title,
                company=company,
                location=location,
                salary=salary,
                job_type=job_type,
                description=description,
            )

        return redirect("jobs")

    search = request.GET.get("search")
    jobs = Job.objects.all()

    if search:
        jobs = jobs.filter(title__icontains=search)

    jobs = jobs.order_by('-id')

    return render(request, "jobs.html", {
        "jobs": jobs
    })


# =========================
# APPLY JOB PAGE
# =========================
@login_required(login_url='auth')
def apply_job(request, id):

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        Application.objects.create(
            job=job,
            name=name,
            email=email,
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            linkedin=request.POST.get("linkedin"),
            cover_letter=request.POST.get("cover_letter"),
            resume=request.FILES.get("resume")
        )

        email_sent = False
        if email:
            try:
                send_mail(
                    subject=f"Application Submitted - {job.title}",
                    message=(
                        f"Hi {name},\n\n"
                        f"Your application for {job.title} at {job.company} "
                        f"was submitted successfully.\n\n"
                        f"We will contact you soon.\n\n"
                        f"Thanks,\nHireHub Team"
                    ),
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
                email_sent = True
            except Exception:
                email_sent = False

        return render(request, "apply_job.html", {
            "job": job,
            "submitted": True,
            "email_sent": email_sent,
        })

    return render(request, "apply_job.html", {
        "job": job
    })


# =========================
# OTHER PAGES
# =========================
def companies(request):
    return render(request, "companies.html")


def premium(request):
    return render(request, "premium.html")


# =========================
# AI JOB SUGGESTION
# =========================
def ai_page(request):

    if request.method == "POST":

        question = request.POST.get("question")

        prompt = f"""
        You are an AI Job Recommendation Assistant.

        Based on the skills provided, return exactly 5 relevant job titles.

        Rules:
        - Return only job titles
        - One job title per line

        Skills: {question}
        """

        jobs_list = get_ai_response(prompt)

        request.session["jobs"] = jobs_list

        return redirect("ai")

    jobs_list = request.session.pop("jobs", [])

    return render(request, "ai.html", {
        "jobs": jobs_list
    })


# =========================
# DELETE RESUME
# =========================
def delete_resume(request, id):

    resume = get_object_or_404(Resume, id=id)

    if resume.resume:
        resume.resume.delete()

    resume.delete()

    return redirect("index")