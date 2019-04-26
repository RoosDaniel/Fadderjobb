from django.urls import path

from . import views


app_name = "trade"

urlpatterns = [
    path('start/<str:receiver_username>/', views.start, name="start"),
    path('<str:other_username>/', views.see_trade, name="see"),
    path('change/<str:other_username>', views.change_trade, name="change"),
]
