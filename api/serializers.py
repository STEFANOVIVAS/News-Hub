from rest_framework import serializers
from noticias.models import Noticia
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class NoticiaSerializer(serializers.ModelSerializer):
    data_noticia = serializers.DateField(input_formats=['%d/%m/%Y'], format='%d/%m/%Y',style={'placeholder': 'Data noticia', 'autofocus': True})
    class Meta:
        model = Noticia
        fields = '__all__'
