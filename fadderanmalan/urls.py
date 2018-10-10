from django.urls import path

from . import views


app_name = "fadderanmalan"

urlpatterns = [
    path('', views.index, name="index"),

    path('jobsignup/', views.jobsignup, name="jobsignup"),
    path('jobsignup/<str:slug>/', views.jobdetails, name="jobsignup_detail"),
    path('jobsignup/register/<int:job_id>/', views.register_for_job, name="jobsignup_register"),
    path('jobsignup/deregister/<int:job_id>/', views.deregister_for_job, name="jobsignup_deregister"),

    path('topchart/', views.topchart, name="topchart"),
]
