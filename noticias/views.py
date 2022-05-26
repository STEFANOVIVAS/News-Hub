from django.shortcuts import render, get_object_or_404
from .models import Noticia
from django.core.paginator import Paginator
from .forms import ShareNoticiaForm,SearchForm
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector
# Create your views here.


def lista_noticias(request):
    noticias = Noticia.objects.all()
    paginator = Paginator(noticias, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'noticias/lista_noticias.html', {'page_obj': page_obj})


def detalha_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)

    return render(request, 'noticias/detalha_noticia.html', {'noticia': noticia})


def procurar_noticias(request):
    form=SearchForm()
    query=None
    results=[]
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results=Noticia.objects.annotate(search=SearchVector('titulo','conteudo'),).filter(search=query)
    return render(request,'noticias/procurar.html',{'form':form,'query':query,'results':results})


def noticias_por_veiculo(request, fonte):
    noticias_veiculo = Noticia.objects.filter(fonte__contains=fonte)
    paginator = Paginator(noticias_veiculo, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'noticias/noticias_por_veiculo.html', {'page_obj': page_obj})


def compartilha_noticia(request, slug):
    noticia = get_object_or_404(Noticia, slug=slug)
    sent = False
    if request.method == 'POST':
        form = ShareNoticiaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(noticia.get_absolute_url())
            subject = f"{cd['nome']} recomenda que você leia" \
                f"{noticia.titulo}"
            message = f" Leia {noticia.titulo} em {post_url} \n\n" \
                f"{cd['nome']}\'s comments: {cd['comentarios']}"
            send_mail(subject, message, 'admin@myblog.com', [cd['send_to']])

            sent = True

    else:
        form = ShareNoticiaForm()
    return render(request, "noticias/compartilha_noticia.html", {'form': form,
                                                                 'noticia': noticia,
                                                                 'sent': sent})
