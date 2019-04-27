from django.urls import path

from .views import renderers, jobregistration

app_name = "fadderanmalan"

urlpatterns = [
    path('', renderers.index, name="index"),

    path('topchart/', renderers.topchart, name="topchart"),

    path('job/list/', renderers.job_list, name="job_list"),
    path('job/<str:slug>/', renderers.job_details, name="job_details"),

    path('job/register/<int:job_id>/', jobregistration.register_for_job,
         name="jobsignup_register"),
    path('job/deregister/<int:job_id>/', jobregistration.deregister_for_job,
         name="jobsignup_deregister"),
]
