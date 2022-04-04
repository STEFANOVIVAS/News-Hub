# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# from scrapy import DjangoItem
from scrapy_djangoitem import DjangoItem
from noticias.models import Noticia


class CrawlingNoticiasItem(DjangoItem):
    django_model = Noticia

    # titulo = scrapy.Field()
    # veiculo = scrapy.Field()
    # data = scrapy.Field()
    # conteudo = scrapy.Field()
    # Url=scrapy.Field()
