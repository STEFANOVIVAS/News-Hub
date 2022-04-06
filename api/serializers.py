from rest_framework import serializers
from noticias.models import Noticia
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'
