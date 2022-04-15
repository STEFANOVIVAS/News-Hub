from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="ArticlesAPI",
      default_version='v1',
      description="Test description",
      
   ),
)



urlpatterns = [path('noticias/', views.NoticiasListView.as_view(), name='list_noticias'),               
               path('noticias/<pk>/', views.NoticiasDetailView.as_view(), name='retrieve_article'),
               # path('<str:fonte>/noticias/', views.NoticiaFonteView.as_view()),               
               path('token/', jwt_views.TokenObtainPairView.as_view(),
                    name='token_obtain_pair'),
               path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
               path('schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),]
