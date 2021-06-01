import scrapy

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawling_noticias.items import CrawlingNoticiasItem

class UolSpider(scrapy.Spider):
    name = 'uol'
    allowed_domains = ['uol.com.br']
    start_urls = ['https://www.uol.com.br']

    #NotImplementedError: UolSpider.parse callback is not defined

    def parse(self,response):
        noticias=response.xpath('//a[@data-menu="menu-noticias"]//@href').getall() #filtrar noticias e economia
        for noticia in noticias:
            yield scrapy.Request(noticia, callback=self.parse_category)
        
        economias=response.xpath('//a[@data-menu="menu-economia"]//@href').getall()
        for economia in economias:
            yield scrapy.Request(economia, callback=self.parse_category)
    
    def parse_category(self,response):
        categorias=response.xpath('//h3[@class="heading-style"]//a//@href').getall()
        for categoria in categorias:
            yield scrapy.Request(categoria, callback=self.parse_news)


    def parse_news(self,response):
        news = response.xpath('//div[@class="thumbnails-wrapper"]//a//@href').getall()
        #('div.thumbnails-wrapper>a::attr(href)').getall()
        for new in news:
            yield scrapy.Request(new, callback=self.parse_conteudo)


    def parse_conteudo(self,response):
        items=CrawlingNoticiasItem()
        
        titulo= response.xpath('//h1/span/i/text()').get()
        data = response.xpath('//p[@class="p-author time"]/text()[1]').get()
        
        conteudos=response.xpath('//div[@class="text  "]//p//text()').getall()
        conteudos_imagem=response.xpath('//div[@class="text has-image "]//p//text()').getall()
        conteudos_especiais= response.xpath('//div[@class="special-text"]//p//text()').getall()
        # if data existe: - será que é por causa da ordem dos comandos?
                                          
        if conteudos and data:
            conteudos_unificados=''.join(conteudos)
           
            items['titulo']=titulo
            items['fonte']='Uol'
            items['data_noticia']=data.split()[0]
            items['conteudo']=conteudos_unificados
            items['url']=response.url
            yield items
                  
        elif conteudos_imagem and data:
            conteudos_imagem_unificados=''.join(conteudos_imagem)
                    
            items['titulo']=titulo
            items['fonte']='Uol'
            items['data_noticia']=data.split()[0]
            items['conteudo']=conteudos_imagem_unificados
            items['url']=response.url
            yield items
                     
        
        elif conteudos_especiais and data:
              conteudos_especiais_unificados=''.join(conteudos_especiais)
              
              items['titulo']=titulo
              items['fonte']='Uol'
              items['data_noticia']=data.split()[0]
              items['conteudo']=conteudos_especiais_unificados
              items['url']=response.url
              yield items

class NoticiasG1Spider(scrapy.Spider):
    name = 'noticias_g1'
    allowed_domains = ['g1.globo.com']
    start_urls = ['https://g1.globo.com']

  
    def parse(self,response):
        links=response.xpath('//li[@class="menu-item"]//a[re:test(@href,"economia|politica|fato|blogs")]//@href').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_category)
            
    def parse_category(self,response):
        sublinks= response.xpath('//div[@class="feed-post-body-title gui-color-primary gui-color-hover "]//@href').getall()
        for sublink in sublinks:
            if "ghtml" in sublink:
                yield scrapy.Request(sublink, callback=self.parse_conteudo)
            else:
                yield scrapy.Request(sublink, callback=self.parse_category)
            
    def parse_conteudo(self,response):
        items=CrawlingNoticiasItem()
        titulo= response.xpath('//h1[@class="content-head__title"]//text()').get()
        data = response.xpath('//time[@itemprop="datePublished"]//text()').get()
        
        conteudos=response.xpath('//p[@class="content-text__container "]//text()').getall()
        if conteudos:
            conteudos_unificados_g1=''.join(conteudos)
            
            
            items['titulo']=titulo
            items['fonte']='Portal G1'
            items['data_noticia']=data.split()[0]
            items['conteudo']=conteudos_unificados_g1
            items['url']=response.url
         
            yield items


class EbcNoticiasSpider(scrapy.Spider):
    name = 'ebc_noticias'
    page_number=1
    allowed_domains = ['ebc.com.br', 'agenciabrasil.ebc.com.br']
    start_urls = ['https://agenciabrasil.ebc.com.br/ultimas?page=0']
    
            
    def parse(self,response):
        
        sublinks= response.xpath("//div[@class='post-item-desc py-0']/a[2]/@href").getall()
        for sublink in sublinks:
            yield response.follow(sublink, callback=self.parse_conteudo)
        
        proxima_pagina = 'https://agenciabrasil.ebc.com.br/ultimas?page='+ str(EbcNoticiasSpider.page_number)
        if EbcNoticiasSpider.page_number <=25:
            EbcNoticiasSpider.page_number += 1
            yield response.follow(proxima_pagina, callback=self.parse)

      
    def parse_conteudo(self, response):
        items=CrawlingNoticiasItem()
        
        titulo = response.xpath("//h2[@class='col-10 offset-1 animated fadeInDown dealy-750 display-6 display-md-4 display-lg-5 font-weight-bold alt-font text-center my-1']//text()").get()
        data = response.xpath("normalize-space(.//h4[@class='col-10 offset-1 animated fadeInDown dealy-1100 alt-font font-italic my-2 small text-info text-center']//text())").get()
        conteudos = response.xpath("//div[@class='post-item-wrap']//p//text()").getall()
        conteudos_unificados=' '.join(conteudos)
        
 
        items['titulo']=titulo
        items['fonte']='Ebc - Agência Brasil'
        items['data_noticia']=data.split()[2]
        items['conteudo']=conteudos_unificados
        items['url']=response.url
 
        yield items


class CamaraNoticiasSpider(scrapy.Spider):
    name = 'camara_noticias'
    allowed_domains = ['camara.leg.br']
    start_urls = ['http://www.camara.leg.br/noticias/ultimas?pagina=1']

     

    def parse(self, response):
                    
        links= response.xpath("//h3[@class='g-chamada__titulo']//@href").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_conteudo)
        
        paginas = response.xpath("//li[@class='pagination-list__nav pagination-list__nav--next ']//a[re:test(@href,'pagina=2|pagina=3|pagina=4|pagina=5|pagina=6|pagina=7')]/@href").get()
        if paginas:
            yield response.follow(url=paginas, callback=self.parse)
            
      
    def parse_conteudo(self, response):
        items=CrawlingNoticiasItem()
        conteudo_inicial=[]
        titulo = response.xpath("//h1[@class='g-artigo__titulo']//text()").get()
        data = response.xpath("normalize-space((.//p[@class='g-artigo__data-hora'])[1]//text())").get()
                
        conteudos= response.xpath("//div[@class='js-article-read-more']//p[2]//following-sibling::p//text()").getall()
        conteudos_2= response.xpath("//div[@align='justify']//p//text()").getall()
        subtitulos= response.xpath("//div[@class='js-article-read-more']//p//strong//text()").getall()
        if conteudos_2: 
        
            for conteudo in conteudos_2:
                  conteudo_inicial.append(conteudo)
        
        else:
            
            for conteudo in conteudos:
                conteudo_inicial.append(conteudo)
            
        
        if subtitulos:
            for subtitulo in subtitulos:
                    if subtitulo in conteudo_inicial:
                        conteudo_inicial.remove(subtitulo)    
        
        conteudos_unificados_camara= ''.join(conteudo_inicial)
        
        items['titulo']=titulo
        items['fonte']='Camara'
        items['data_noticia']=data.split("-")[0]
        items['conteudo']=conteudos_unificados_camara
        items['url']=response.url
 
        yield items        
        
        

        
class SenadoNoticiasSpider(scrapy.Spider):
    name = 'senado_noticias'
    allowed_domains = ['senado.leg.br']
    start_urls = ['https://www12.senado.leg.br/noticias/ultimas']

    def parse(self, response):
        
        links_audio= response.xpath("//span[@class='glyphicon glyphicon-volume-up']//following-sibling::a//@href").getall()
        for link in links_audio:
            yield response.follow(url=link, callback=self.parse_conteudo)
        links_texto= response.xpath("//span[@class='glyphicon glyphicon-list-alt']//following-sibling::a//@href").getall()        
        for link in links_texto:
            yield response.follow(url=link, callback=self.parse_conteudo)
        
        paginas = response.xpath("//li[@class='active']//following-sibling::li//a[re:test(@href,'ultimas/2|ultimas/3|ultimas/4|ultimas/5|ultimas/6')]/@href").get()
        if paginas:
            yield scrapy.Request (paginas, callback=self.parse)
         
            
    def parse_conteudo(self, response):
        items=CrawlingNoticiasItem()
        # conteudo_inicial=[]
        titulo = response.xpath("//h1//text()").get()
        data = response.xpath("//span[@class='text-muted']//text()").get()
        conteudos= response.xpath("//div[@id='textoMateria']//p//text()").getall()
        
        if conteudos:
            conteudos_unificados_senado= ''.join(conteudos)
                    
            items['titulo']=titulo
            items['fonte']='Senado'
            items['data_noticia']=data.split(",")[0]
            items['conteudo']=conteudos_unificados_senado
            items['url']=response.url
 
            yield items





process = CrawlerProcess(settings=get_project_settings())
process.crawl(UolSpider)
process.crawl(NoticiasG1Spider)
process.crawl(EbcNoticiasSpider)
process.crawl(CamaraNoticiasSpider)
process.crawl(SenadoNoticiasSpider)
process.start(stop_after_crawl=True)

#stop_after_crawl=False)

# sqlite3.IntegrityError: UNIQUE constraint failed: noticias_noticia.titulo
# django.db.utils.IntegrityError: UNIQUE constraint failed: noticias_noticia.titulo