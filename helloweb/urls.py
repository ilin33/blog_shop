from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("datetime/", views.current_datetime, name="datetime"),
    path("datatime_class/", views.CurrentDatetime.as_view(), name="CurrentDatetime_class"),
    path("date/<str:anything>", views.current_datetime, name="date")
]
