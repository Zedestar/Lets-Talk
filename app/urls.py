from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView

# Creating the path here

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<slug:slug>', views.post_page, name="post_page"),
    path('tag/<slug:slug>', views.tag_page, name="tag_page"),
    path('author/<slug:slug>', views.author_page, name="author_page"),
    path('bookmarks/<slug:slug>', views.bookmarks_page, name="bookmarks"),
    path('like/<slug:slug>', views.like_page, name="like"),
    path('delete/<slug:slug>', views.delete_post, name="delete_post"),
    path('all_bookmark_page', views.all_bookmark_page, name="all_bookmark_page"),
    path('all_likes_page', views.my_likes_page, name="all_likes_page"),
    path('all_posts', views.all_posts, name="all_post"),
    path('new_post', views.new_post, name="new_post"),
    path('create_profile', views.create_profile, name="create_profile"),
    path('edit_profile/<int:pk>', views.edit_profile, name="edit_profile"),
    path('search', views.search_page, name="search"),
    path('about', views.about_page, name="about"),
    path('accounts/register', views.register_page, name="register"),
    path('logout', views.logout_page, name="logoutt"),
]