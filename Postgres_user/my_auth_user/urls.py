from django.urls import path
from .views import GetUsersView, RegisterView, LoginView, SyncAllUsersView, SyncUsersView, UserDetailsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('sync-users/', SyncUsersView.as_view(), name='sync-users'),
    path('get-users/', GetUsersView.as_view(), name='get-users'),
    path('sync_allusers/', SyncAllUsersView.as_view(), name='sync-users'),

]
