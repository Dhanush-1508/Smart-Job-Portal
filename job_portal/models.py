from django.db import models


class Job(models.Model):
    JOB_TYPES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    )

    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Resume(models.Model):
    resume = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resume.name


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    linkedin = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='applications/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"

class Resume(models.Model):
        resume = models.FileField(upload_to='resumes/')
        uploaded_at = models.DateTimeField(auto_now_add=True)
        ats_score = models.IntegerField(null=True, blank=True)