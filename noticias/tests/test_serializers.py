from datetime import date

from rest_framework.test import APITestCase 
from noticias.models import Noticia
from api.serializers import NoticiaSerializer
from rest_framework.fields import DateField

class TestNoticiaSerializer(APITestCase):
    
    def setUp(self):

        
        self.atributos_noticia = {
            'id':'1',
            'titulo':'Guerra entre Russia e ucrania', 
            'data_noticia':date.fromisoformat('2021-11-16'), 
            'fonte':'Uol', 
            'conteudo':'Guerra entre russia e ucrania deixa milhares de feridos',
            'url': 'https://www.uol.com.br/guerra-entre-russia',
            'slug':'guerra-entre-russia-e-ucrania',
        }

        

        self.noticia = Noticia.objects.create(**self.atributos_noticia)
        self.serializer = NoticiaSerializer(instance=self.noticia)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id','titulo', 'data_noticia','fonte','conteudo','url','slug']))

    def test_titulo_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['titulo'], self.atributos_noticia['titulo'])

    def test_data_noticia_field_content(self):
        data = self.serializer.data
        
        self.assertEqual(data['data_noticia'], self.atributos_noticia['data_noticia'].strftime("%d/%m/%Y"))

    def test_fonte_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['fonte'], self.atributos_noticia['fonte'])

    def test_conteudo_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['conteudo'], self.atributos_noticia['conteudo'])

    def test_url_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['url'], self.atributos_noticia['url'])

    def test_slug_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['slug'], self.atributos_noticia['slug'])

  