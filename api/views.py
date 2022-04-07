from django.shortcuts import render
from rest_framework import generics,filters
from api.serializers import NoticiaSerializer
from noticias.models import Noticia
from rest_framework.views import APIView
import django_filters 


# Create your views here.

CHOICES=(('Uol','Uol'),('Ebc','Ebc'),('Portal_G1','Portal G1'),)
class NoticiasFilter(django_filters.FilterSet):
    
    fonte = django_filters.MultipleChoiceFilter(choices = CHOICES)

    class Meta:
        model = Noticia
        fields ={'fonte':['exact'], 
        'data_noticia':['lte','gte'],}
        

class NoticiasListView(generics.ListAPIView):
    queryset=Noticia.objects.all()
    serializer_class = NoticiaSerializer
    
    filterset_class=NoticiasFilter
    search_fields=['titulo','conteudo']


class NoticiasDetailView(generics.RetrieveAPIView):
    queryset = Noticia.objects.all()
    serializer_class = NoticiaSerializer


# class NoticiaFonteView(generics.ListAPIView):
#     serializer_class=NoticiaSerializer

#     def get_queryset(self):
#         queryset=Noticia.objects.all()
#         fonte=self.kwargs['fonte']
#         if fonte:
#             queryset=Noticia.objects.filter(fonte=fonte)
#         return queryset

       
        