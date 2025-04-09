from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:title>/", views.post, name="post"),
    path("category/<str:name>/", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("create-post/", views.create_post, name="create_post"),
    path('login/', LoginView.as_view(), name='blog_login'),
    path('logout/', LogoutView.as_view(), name='blog_logout')
]
