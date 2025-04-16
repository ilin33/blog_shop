from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import profile_view, login_view, logout_view, register_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:title>/", views.post, name="post"),
    path("category/<str:name>/", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("create-post/", views.create_post, name="create_post"),
    path('login/', login_view, name='blog_login'),
    path('logout/', logout_view, name='blog_logout'),
    path('profile/', profile_view, name='profile'),
    path('tag/<str:name>/', views.tag, name='tag'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('post/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('register/', register_view, name='register'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)