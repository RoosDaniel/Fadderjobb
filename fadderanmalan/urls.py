from django.urls import path

from .views import renderers, jobregistration

app_name = "fadderanmalan"

urlpatterns = [
    path('', renderers.index, name="index"),

    path('jobsignup/', renderers.jobsignup, name="jobsignup"),
    path('jobsignup/<str:slug>/', renderers.jobdetails, name="jobsignup_detail"),
    path('topchart/', renderers.topchart, name="topchart"),

    path('jobsignup/register/<int:job_id>/', jobregistration.register_for_job,
         name="jobsignup_register"),
    path('jobsignup/deregister/<int:job_id>/', jobregistration.deregister_for_job,
         name="jobsignup_deregister"),
]
