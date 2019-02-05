from django.urls import path

from .views import JobFeed


app_name = "job_calendar"

urlpatterns = [
    path('<str:user>.ics/', JobFeed(), name="get_calendar")
]
