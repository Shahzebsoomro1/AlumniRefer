from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:pk>/', views.profile_view, name='profile_detail'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('alumni/', views.alumni_list_view, name='alumni_list'),
]
