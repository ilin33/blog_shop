from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:title>/", views.post, name="post"),
    path("category/<str:name>/", views.category, name="category"),
    path("search/", views.search, name="search")
]
