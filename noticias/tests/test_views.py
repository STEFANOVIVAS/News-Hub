import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from noticias.models import Noticia
from api.serializers import NoticiaSerializer
from users.models import NewUser
from rest_framework.test import force_authenticate
from rest_framework.test import APITestCase,force_authenticate,APIRequestFactory,APIClient
from api.views import *
from rest_framework_simplejwt.tokens import RefreshToken




class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('users:create-user')
        data = {'email': 'kelzinha@hotmail.com','password':'34992084rfg','user_name':'kelzinha','first_name':'Raquel'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewUser.objects.count(), 1)
        self.assertEqual(NewUser.objects.get().user_name, 'kelzinha')



class ListArticlesTest(APITestCase):
    """ Test module for GET all news API """

    def setUp(self):
        Noticia.objects.create(
            titulo='Guerra entre Russia e ucrania', data_noticia='2021-11-16', fonte='Uol', conteudo='Guerra entre russia e ucrania deixa milhares de feridos')
        Noticia.objects.create(
            titulo='São paulo goleia Athletico-Pr', data_noticia='2022-04-11', fonte='Ebc', conteudo='Em jogo de muita facilidade São paulo goleio athetlico e se mantem na liderança')
        Noticia.objects.create(
            titulo='Alckim é escolhe como vice de Lula', data_noticia='2022-04-09', fonte='Portal_g1', conteudo='Geraldo alckmin se filia ao PSB e anuncia sua candidatura a vice presidente da república')
        
        self.test_user1 = NewUser.objects.create_user(email='testuser1@gmail.com', user_name='testuser1', password='1X<ISRUkw+tuK', first_name='teste')
        self.test_user1.save()

        self.factory=APIRequestFactory()

    def test_list_noticias_view_status_code_200(self):
        response = self.client.get(reverse('list_noticias'))
        noticias = Noticia.objects.all()
        serializer = NoticiaSerializer(noticias, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)
    
    
    


class RetrieveArticleTest(APITestCase):
    def setUp(self):
        Noticia.objects.create(
            titulo='Guerra entre Russia e ucrania', data_noticia='2021-11-16', fonte='Uol', conteudo='Guerra entre russia e ucrania deixa milhares de feridos')
        test_user1 = NewUser.objects.create_user(email='testuser1@gmail.com', user_name='testuser1', password='1X<ISRUkw+tuK', first_name='teste')
        test_user1.save()
        self.client = APIClient()
        refresh = RefreshToken.for_user(test_user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


    def test_retrieve_article_with_authentication_status_code_200(self):
        noticia = Noticia.objects.get(titulo='Guerra entre Russia e ucrania')
        url = reverse('retrieve_article',kwargs={'pk':noticia.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_single_article_data(self):
        noticia = Noticia.objects.get(titulo='Guerra entre Russia e ucrania')
        url = reverse('retrieve_article',kwargs={'pk':noticia.pk})
        response = self.client.get(url)
        
        serializer = NoticiaSerializer(noticia)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    
    
    def test_get_invalid_single_article(self):
        response = self.client.get(
            reverse('retrieve_article', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
      
        
