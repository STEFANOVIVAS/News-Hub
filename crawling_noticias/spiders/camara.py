import scrapy
from crawling_noticias.items import CrawlingNoticiasItem


class CamaraNoticiasSpider(scrapy.Spider):
    name = 'camara_noticias'
    allowed_domains = ['camara.leg.br']
    start_urls = ['http://www.camara.leg.br/noticias/ultimas?pagina=1']

    def parse(self, response):

        links = response.xpath(
            "//h3[@class='g-chamada__titulo']//@href").getall()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_conteudo)

        paginas = response.xpath(
            "//li[@class='pagination-list__nav pagination-list__nav--next ']//a[re:test(@href,'pagina=2|pagina=3|pagina=4|pagina=5|pagina=6|pagina=7')]/@href").get()
        if paginas:
            yield response.follow(url=paginas, callback=self.parse)

    def parse_conteudo(self, response):
        items = CrawlingNoticiasItem()
        conteudo_inicial = []
        titulo = response.xpath(
            "//h1[@class='g-artigo__titulo']//text()").get()
        raw_data = response.xpath(
            "normalize-space(.//p[@class='g-artigo__data-hora'][1]//text())").get()
        data = raw_data.split("-")[0]
        conteudos = response.xpath(
            "//div[@class='js-article-read-more']//p[2]//following-sibling::p//text()").getall()
        conteudos_2 = response.xpath(
            "//div[@align='justify']//p//text()").getall()
        subtitulos = response.xpath(
            "//div[@class='js-article-read-more']//p//strong//text()").getall()
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

        conteudos_unificados_camara = ''.join(conteudo_inicial)

        items['titulo'] = titulo
        items['fonte'] = 'Camara'
        items['data_noticia'] = data.replace(" ", "")
        items['conteudo'] = conteudos_unificados_camara
        items['url'] = response.url

        yield items
