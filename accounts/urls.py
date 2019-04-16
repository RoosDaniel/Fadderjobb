from django.urls import path

import cas.views

from loginas.views import user_logout

from . import views


app_name = "accounts"

urlpatterns = [
    path('login/', cas.views.login, name="login"),
    path('logout/', cas.views.logout, name="logout"),
    path('restore/', views.restore_impersonation, name="restore"),

    path('my_profile/', views.my_profile, name="my_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('profile/<str:username>', views.profile, name="profile"),
]
