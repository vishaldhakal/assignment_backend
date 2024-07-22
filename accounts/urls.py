from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('change-password/', views.ChangePasswordView.as_view(),
         name='change-password'),
    path("api-token-auth/", views.CustomAuthToken.as_view(), name="api_token_auth"),
    path("get-agent/", views.get_agent, name="get_agent"),
    path('update-img/', views.updateImageApi, name='updateimgapi'),
    path('update-profile/', views.updateProfile, name='updateprof'),
    path('register-agent/', views.register_agent, name='register_agent'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
]
