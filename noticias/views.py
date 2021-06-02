from django.shortcuts import render, get_object_or_404
from .models import Noticia
from django.core.paginator import Paginator

# Create your views here.


def lista_noticias(request):
    noticias = Noticia.objects.order_by('-data_noticia')
    paginator = Paginator(noticias, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'noticias/lista_noticias.html', {'page_obj': page_obj})


def detalha_noticias(request, slug):
    noticias = get_object_or_404(Noticia, slug=slug)

    return render(request, 'noticias/detalha_noticias.html', {'noticias': noticias})


def procurar_noticias(request):
    lista_noticias = Noticia.objects.order_by('-data_noticia')
    if 'buscar' in request.GET:
        procurar_noticias = request.GET['buscar']
        if procurar_noticias:
            lista_noticias = lista_noticias.filter(
                conteudo__icontains=procurar_noticias)

    dados = {
        'noticias': lista_noticias
    }

    return render(request, 'noticias/procurar.html', dados)


def noticias_por_veiculo(request, fonte):
    noticias_veiculo = Noticia.objects.filter(fonte__contains=fonte)
    return render(request, 'noticias/noticias_por_veiculo.html', {'noticias_veiculo': noticias_veiculo})
