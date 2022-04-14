from django.test import TestCase
from django.utils.text import slugify

from noticias.models import Noticia

class NoticiaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        noticia=Noticia.objects.create(
            titulo='Guerra entre Russia e ucrania', 
            data_noticia='2021-11-16', fonte='Uol', 
            conteudo='Guerra entre russia e ucrania deixa milhares de feridos',
            )
        noticia.slug=slugify(noticia.titulo)
        noticia.save()
    
    
    def test_titulo_max_length(self):
        noticia = Noticia.objects.get(id=1)
        max_length = noticia._meta.get_field('titulo').max_length
        self.assertEquals(max_length, 200)

    def test_fonte_max_length(self):
       noticia = Noticia.objects.get(id=1)
       max_length = noticia._meta.get_field('fonte').max_length
       self.assertEquals(max_length, 50)


    def test_object_name_is_titulo_name(self):
        noticia = Noticia.objects.get(id=1)
        expected_object_name = f'{noticia.titulo}'
        self.assertEquals(expected_object_name, str(noticia))

    def test_get_absolute_url(self):
        noticia = Noticia.objects.get(id=1)
        noticia_slug=slugify(noticia.titulo)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(noticia.get_absolute_url(), f'/noticias/{noticia_slug}/')