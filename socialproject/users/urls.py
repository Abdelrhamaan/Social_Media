from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
# from posts.views import add_comment

''' if you didnt pass template_name he will rederict you to 
        django template view '''
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name="users/login.html"), name='logout'),
    path('password_change/', auth_view.PasswordChangeView.as_view(
        template_name="users/password_change.html"), name="password_change"),
    path('passeword_change/done/', auth_view.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"), name="password_change_done"),
    path('password_reset/', auth_view.PasswordResetView.as_view(
        template_name="users/password_reset.html"), name="password_reset"),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name="users/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset/complete', auth_view.PasswordResetCompleteView.as_view(
        template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    path('register/', views.register, name='register'),
    path('edit/', views.edit_user_profile, name='edit_user_profile'),
    path('profile/', views.profile, name='profile'),
    # path('add_comment/', add_comment, name='add_comment'),

]
