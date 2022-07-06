from django.urls import path

from apps.jwt_authentication import views


urlpatterns = [
    path('refresh-token/', views.RefreshTokenAPIView.as_view()),

]
