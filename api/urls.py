from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [path('noticias/', views.NoticiasListView.as_view(), name='list_noticias'),               
               path('noticias/<pk>/', views.NoticiasDetailView.as_view(), name='retrieve_article'),
               # path('<str:fonte>/noticias/', views.NoticiaFonteView.as_view()),               
               path('token/', jwt_views.TokenObtainPairView.as_view(),
                    name='token_obtain_pair'),
               path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh')]
