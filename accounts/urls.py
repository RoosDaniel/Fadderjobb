from django.urls import path

import cas.views

from . import views


app_name = "accounts"

urlpatterns = [
    path('login/', cas.views.login, name="login"),
    path('logout/', cas.views.logout, name="logout"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('profile/<str:username>', views.profile, name="profile"),
    # path('registration/', views.registration, name="registration"),
]
