from django.urls import path
from . import views


urlpatterns = [path('noticias/', views.NoticiasListView.as_view()),
               path('noticias/<pk>/', views.NoticiasDetailView.as_view()), ]
