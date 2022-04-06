from django.shortcuts import render
from rest_framework import generics
from api.serializers import NoticiaSerializer
from noticias.models import Noticia
from rest_framework.views import APIView

# Create your views here.


class NoticiasListView(generics.ListAPIView):
    queryset=Noticia.objects.all()
    serializer_class = NoticiaSerializer


class NoticiasDetailView(generics.RetrieveAPIView):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


class NoticiaFonteView(generics.ListAPIView):
    serializer_class=NoticiaSerializer

    def get_queryset(self):
        queryset=Noticia.objects.all()
        fonte=self.kwargs['fonte']
        if fonte:
            queryset=Noticia.objects.filter(fonte=fonte)
        return queryset

       
        