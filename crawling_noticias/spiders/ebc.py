import scrapy
from crawling_noticias.items import CrawlingNoticiasItem


class EbcNoticiasSpider(scrapy.Spider):
    name = 'ebc_noticias'
    page_number = 1
    allowed_domains = ['ebc.com.br', 'agenciabrasil.ebc.com.br']
    start_urls = ['https://agenciabrasil.ebc.com.br/ultimas?page=0']

    def parse(self, response):

        sublinks=response.xpath("//div[@class='post-item-desc py-0']/a[2][re:test(@href,'economia')]//@href").getall()
        # sublinks = response.xpath(
        #     "//div[@class='post-item-desc py-0']/a[2]/@href").getall()
        for sublink in sublinks:
            yield response.follow(sublink, callback=self.parse_conteudo)

        proxima_pagina = 'https://agenciabrasil.ebc.com.br/ultimas?page=' + \
            str(EbcNoticiasSpider.page_number)
        if EbcNoticiasSpider.page_number <= 5:
            EbcNoticiasSpider.page_number += 1
            yield response.follow(proxima_pagina, callback=self.parse)

    def parse_conteudo(self, response):
        items = CrawlingNoticiasItem()

        titulo = response.xpath(
            "//h2[@class='col-10 offset-1 animated fadeInDown dealy-750 display-6 display-md-4 display-lg-5 font-weight-bold alt-font text-center my-1']//text()").get()
        data = response.xpath(
            "normalize-space(.//h4[@class='col-10 offset-1 animated fadeInDown dealy-1100 alt-font font-italic my-2 small text-info text-center']//text())").get()
        data_clean=data.split(' -')[0]
        
        
        
        conteudos = response.xpath(
            "//div[@class='post-item-wrap']//p//text()").getall()
        conteudos_unificados = ' '.join(conteudos)

        # yield {
        #         'titulo' : titulo,
        #         'fonte' : 'Ebc - Agência Brasil',
        #         'data_noticia' : data,
        #         'conteudo' : conteudos_unificados,
        #         'url' : response.url,


        # }

        items['titulo'] = titulo
        items['fonte'] = 'Uol'
        items['data_noticia'] = data_clean.split(' ')[-1]
        items['conteudo'] = conteudos_unificados
        items['url'] = response.url
        yield items
       

        
