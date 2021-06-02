
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from crawling_noticias.spiders.ebc import EbcNoticiasSpider
from crawling_noticias.spiders.camara import CamaraNoticiasSpider
from crawling_noticias.spiders.uol import UolSpider
from crawling_noticias.spiders.senado import SenadoNoticiasSpider
from crawling_noticias.spiders.g1 import NoticiasG1Spider

from apscheduler.schedulers.twisted import TwistedScheduler

process = CrawlerProcess(get_project_settings())
# process.crawl(UolSpider)
# process.crawl(NoticiasG1Spider)
# process.crawl(EbcNoticiasSpider)
# process.crawl(CamaraNoticiasSpider)
# process.crawl(SenadoNoticiasSpider)
# process.start(stop_after_crawl=True)


scheduler = TwistedScheduler()
scheduler.add_job(process.crawl, 'interval', args=[
                  CamaraNoticiasSpider], minutes=10)
scheduler.add_job(process.crawl, 'interval', args=[
                  EbcNoticiasSpider], minutes=10)
scheduler.add_job(process.crawl, 'interval', args=[
                  NoticiasG1Spider], minutes=40)
scheduler.add_job(process.crawl, 'interval', args=[
                  SenadoNoticiasSpider], minutes=10)
scheduler.add_job(process.crawl, 'interval', args=[
                  UolSpider], minutes=40)


scheduler.start()
process.start(False)
