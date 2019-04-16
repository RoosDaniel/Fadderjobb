from django.urls import path

from . import views


app_name = "trade"

urlpatterns = [
    path('start/<str:receiver_username>/', views.start, name="start"),
    path('complete/<str:sender_username>/', views.complete, name="complete"),
]
