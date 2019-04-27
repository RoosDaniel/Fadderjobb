from django.urls import path

from .views import renderers, jobregistration

app_name = "fadderanmalan"

urlpatterns = [
    path('list/', renderers.job_list, name="job_list"),
    path('<str:slug>/', renderers.job_details, name="job_details"),

    path('register/<int:job_id>/', jobregistration.register_for_job,
         name="jobsignup_register"),
    path('deregister/<int:job_id>/', jobregistration.deregister_for_job,
         name="jobsignup_deregister"),
]
