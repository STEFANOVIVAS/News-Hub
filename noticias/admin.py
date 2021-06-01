from django.contrib import admin
from .models import Noticia

class ListandoNoticias(admin.ModelAdmin):
    list_display=('id','titulo','data_noticia','fonte', 'conteudo', 'url', 'slug')
    list_display_links=('id','titulo', 'conteudo')
    search_fields=('titulo', 'conteudo',)
    list_filter=('data_noticia', 'fonte',)
    list_per_page=20
    prepopulated_fields = {"slug": ("titulo",)}



admin.site.register(Noticia, ListandoNoticias)

