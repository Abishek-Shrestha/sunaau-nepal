from django.urls import path

from . import views


urlpatterns = [
	path("", views.home_view, name="home"),
	path('dashboard/', views.municipality_dashboard, name='municipality_dashboard'),
    path('my-reports/', views.my_reports, name='my_reports'),
]
