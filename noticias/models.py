from django.db import models
from django.conf import settings
from django.urls import reverse


class Noticia(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    data_noticia = models.DateField()
    fonte = models.CharField(max_length=50)
    conteudo = models.TextField()
    url = models.URLField()
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("noticias:detalha_noticia", kwargs={"slug": self.slug})
