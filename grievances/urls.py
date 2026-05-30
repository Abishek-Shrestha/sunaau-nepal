from django.urls import path

from . import views


urlpatterns = [
	path("", views.home_view, name="home"),
    path('report/', views.report_issue, name='report_issue'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
	path('dashboard/', views.municipality_dashboard, name='municipality_dashboard'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
]
