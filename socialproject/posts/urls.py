from django.urls import path
from . import views


# app_name = 'posts'

urlpatterns = [
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_user_post'),
    path('like', views.liked_posts, name='like'),
    # path('add_comment/', views.add_comment, name='comment'),
    # path('add_comment/', views.add_comment, name='add_comment'),
]
