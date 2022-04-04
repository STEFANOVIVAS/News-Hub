import scrapy
from crawling_noticias.items import CrawlingNoticiasItem


class UolSpider(scrapy.Spider):
    name = 'uol'
    allowed_domains = ['uol.com.br']
    start_urls = ['https://www.uol.com.br']

    # NotImplementedError: UolSpider.parse callback is not defined

    def parse(self, response):
        # filtrar noticias e economia
        # noticias = response.xpath(
        #     '//a[@data-menu="menu-noticias"]//@href').getall()
        # for noticia in noticias:
        #     yield scrapy.Request(noticia, callback=self.parse_category)

        economias = response.xpath(
            # '//a[@data-menu="menu-economia"]//@href').get()
        '//li[@class="menuDesktop__item menuDesktop__item--economia"]//div[@class="menuDesktop__submenu"]//@href').getall()
        for economia in economias:
            yield scrapy.Request(economia, callback=self.parse_category)

    def parse_category(self, response):
        categorias = response.xpath(
            '//h3[@class="heading-style"]//a//@href').getall()
        for categoria in categorias:
            yield scrapy.Request(categoria, callback=self.parse_news)

    def parse_news(self, response):
        news = response.xpath(
            '//div[@class="thumbnails-wrapper"]//a//@href').getall()
        # ('div.thumbnails-wrapper>a::attr(href)').getall()
        for new in news:
            yield scrapy.Request(new, callback=self.parse_conteudo)

    def parse_conteudo(self, response):
        items = CrawlingNoticiasItem()
        if '2022' in response.url:
            titulo = response.xpath('//h1/span//i//text()').get()
            data = response.xpath('//p[@class="p-author time"]/text()[1]').get()
            
            conteudos = response.xpath(
                '//div[@class="text  "]//p//text()').getall()
            conteudos_imagem = response.xpath(
                '//div[@class="text has-image "]//p//text()').getall()
            conteudos_especiais = response.xpath(
                '//div[@class="special-text"]//p//text()').getall()
            # if data existe: - será que é por causa da ordem dos comandos?

            if conteudos and data:
                conteudos_unificados = ''.join(conteudos)

                # yield{

                #     'titulo': titulo,
                #     'fonte':'Uol',
                #     'data_noticia':data,
                #     'conteudo':conteudos_unificados,
                #     'url':response.url
                # }
                items['titulo'] = titulo
                items['fonte'] = 'Uol'
                items['data_noticia'] = data.split()[0]
                items['conteudo'] = conteudos_unificados
                items['url'] = response.url
                yield items

            elif conteudos_imagem and data:
                conteudos_imagem_unificados = ''.join(conteudos_imagem)

                # yield{

                #     'titulo': titulo,
                #     'fonte':'Uol',
                #     'data_noticia':data,
                #     'conteudo':conteudos_imagem_unificados,
                #     'url':response.url
                # }
                items['titulo'] = titulo
                items['fonte'] = 'Uol'
                items['data_noticia'] = data.split()[0]
                items['conteudo'] = conteudos_imagem_unificados
                items['url'] = response.url
                yield items

            elif conteudos_especiais and data:
                conteudos_especiais_unificados = ''.join(conteudos_especiais)

                # yield{

                #     'titulo': titulo,
                #     'fonte':'Uol',
                #     'data_noticia':data,
                #     'conteudo':conteudos_especiais_unificados,
                #     'url':response.url
                # }
                items['titulo'] = titulo
                items['fonte'] = 'Uol'
                items['data_noticia'] = data.split()[0]
                items['conteudo'] = conteudos_especiais_unificados
                items['url'] = response.url
                yield items
