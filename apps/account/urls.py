from django.urls import path

from apps.account import views


urlpatterns = [
    path('user/<uuid>/', views.UserAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view())
]
