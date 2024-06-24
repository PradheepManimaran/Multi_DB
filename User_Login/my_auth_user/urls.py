from django.urls import path
from .views import RegisterView, LoginView, UserDetailsView, welcome_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('userlogin/', welcome_view, name='welcome'),

]
