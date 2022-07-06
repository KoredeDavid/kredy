from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),

    path('articles-factory/<username>/', views.articles_factory, name='articles_factory'),

]
