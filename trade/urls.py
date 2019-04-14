from django.urls import path

from . import views


app_name = "trade"

urlpatterns = [
    path('<str:receiver_username>/', views.trade, name="start"),
]
