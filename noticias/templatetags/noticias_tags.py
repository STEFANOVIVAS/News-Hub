from django import template
from ..models import Noticia

register=template.Library()

@register.inclusion_tag('noticias/noticias_por_veiculo.html')
def listar_materias_por_veiculo (fonte):
    noticias_veiculos= Noticia.objects.filter(fonte=fonte).order_by('-data_noticia')
    return {'noticias_veiculos':noticias_veiculos}