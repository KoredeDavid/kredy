from django.urls import path

from apps.account import views


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),

    path('verify-email/', views.VerifyEmailAPIView.as_view(), name='verify-email')
]
