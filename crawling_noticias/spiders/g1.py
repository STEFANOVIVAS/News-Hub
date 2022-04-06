import scrapy
from crawling_noticias.items import CrawlingNoticiasItem


class NoticiasG1Spider(scrapy.Spider):
    name = 'noticias_g1'
    allowed_domains = ['g1.globo.com']
    start_urls = ['https://g1.globo.com']

    def parse(self, response):

        links = response.xpath('//li[@id="menu-2-economia"]/ul//li//a/@href').getall()
        # links = response.xpath(
        #     '//li[@class="menu-item"]//a[re:test(@href,"economia|politica|fato|blogs")]//@href').getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_category)

    def parse_category(self, response):
        sublinks = response.xpath(
            '//div[@class="feed-post-body-title gui-color-primary gui-color-hover "]//@href').getall()
        for sublink in sublinks:
            if "ghtml" in sublink:
                yield scrapy.Request(sublink, callback=self.parse_conteudo)
            else:
                yield scrapy.Request(sublink, callback=self.parse_category)

    def parse_conteudo(self, response):
         if '2022' in response.url:
            items = CrawlingNoticiasItem()
            titulo = response.xpath(
                '//h1[@class="content-head__title"]//text()').get()
            data = response.xpath(
                '//time[@itemprop="datePublished"]//text()').get()

            conteudos = response.xpath(
                '//p[@class="content-text__container "]//text()').getall()
            
            
            if conteudos:
                conteudos_unificados_g1 = ''.join(conteudos)

                # yield{
                #         'titulo': titulo,
                #         'fonte' :'Portal G1',
                #         'data_noticia' : data,
                #         'conteudo' : conteudos_unificados_g1,
                #         'url' : response.url


                # }
            
                items['titulo'] = titulo
                items['fonte'] = 'Portal_G1'
                items['data_noticia'] = data.split()[0]
                items['conteudo'] = conteudos_unificados_g1
                items['url'] = response.url
                yield items
