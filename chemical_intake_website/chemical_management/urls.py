from django.urls import path

from . import views

urlpatterns = [
    path("entry", views.entryform, name="entryform"),
    path("report", views.report, name="report"),
    path("report/daily", views.daily_report, name="daily_report"),
    path("report/monthly", views.monthly_report, name="monthly_report"),
    path("analytics", views.analytics, name="analytics"),
    path("settings", views.settings, name="settings"),
    path("", views.user_logout, name="user_logout"),
]
