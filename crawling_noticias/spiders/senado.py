import scrapy
from crawling_noticias.items import CrawlingNoticiasItem


class SenadoNoticiasSpider(scrapy.Spider):
    name = 'senado_noticias'
    allowed_domains = ['senado.leg.br']
    start_urls = ['https://www12.senado.leg.br/noticias/ultimas']

    def parse(self, response):

        links_audio = response.xpath(
            "//span[@class='glyphicon glyphicon-volume-up']//following-sibling::a//@href").getall()
        for link in links_audio:
            yield response.follow(url=link, callback=self.parse_conteudo)
        links_texto = response.xpath(
            "//span[@class='glyphicon glyphicon-list-alt']//following-sibling::a//@href").getall()
        for link in links_texto:
            yield response.follow(url=link, callback=self.parse_conteudo)

        paginas = response.xpath(
            "//li[@class='active']//following-sibling::li//a[re:test(@href,'ultimas/2|ultimas/3|ultimas/4|ultimas/5|ultimas/6')]/@href").get()
        if paginas:
            yield scrapy.Request(paginas, callback=self.parse)

    def parse_conteudo(self, response):
        items = CrawlingNoticiasItem()
        # conteudo_inicial=[]
        titulo = response.xpath("//h1//text()").get()
        data = response.xpath("//span[@class='text-muted']//text()").get()
        conteudos = response.xpath(
            "//div[@id='textoMateria']//p//text()").getall()

        if conteudos:
            conteudos_unificados_senado = ''.join(conteudos)

            items['titulo'] = titulo
            items['fonte'] = 'Senado'
            items['data_noticia'] = data.split(",")[0]
            items['conteudo'] = conteudos_unificados_senado
            items['url'] = response.url

            yield items
