from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegistionView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('get_profile/', views.get_profile),
    path ('actions/',views.ActionView.as_view()),
]