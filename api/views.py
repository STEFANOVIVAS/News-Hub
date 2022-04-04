from django.shortcuts import render
from rest_framework import generics
from api.serializers import NoticiaSerializer
from noticias.models import Noticia

# Create your views here.


class NoticiasListView(generics.ListAPIView):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class NoticiasDetailView(generics.RetrieveAPIView):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer
