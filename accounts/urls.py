from django.urls import path

from . import views

app_name = "accounts"


urlpatterns = [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('profile/<str:liu_id>', views.profile, name="profile"),
    path('registration/', views.registration, name="registration"),
]
