from django.urls import path
from . import views


app_name = 'noticias'

urlpatterns = [
    path("", views.lista_noticias, name="lista_noticias"),
    path("<slug:slug>/", views.detalha_noticia, name="detalha_noticia"),
    path("procurar/", views.procurar_noticias, name="procurar_noticias"),
    path("<str:fonte>", views.noticias_por_veiculo, name="noticias_por_veiculo"),
    path("<slug:slug>/compartilha_noticia",
         views.compartilha_noticia, name="compartilha_noticia")
]
