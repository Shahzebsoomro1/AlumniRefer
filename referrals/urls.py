from django.urls import path
from . import views

app_name = 'referrals'

urlpatterns = [
    path('request/<int:job_pk>/', views.request_referral_view, name='request'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
    path('withdraw/<int:pk>/', views.withdraw_request_view, name='withdraw'),
    path('incoming/', views.incoming_requests_view, name='incoming'),
    path('respond/<int:pk>/', views.respond_to_request_view, name='respond'),
    path('admin/manage/', views.admin_manage_view, name='admin_manage'),
    path('admin/outcome/<int:pk>/', views.mark_outcome_view, name='mark_outcome'),
]
