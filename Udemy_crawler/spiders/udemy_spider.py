import scrapy
from scrapy.http import FormRequest

class UdemySpiderSpider(scrapy.Spider):
    name = "udemy_spider"
    allowed_domains = ["udemy.com"]
    start_urls = ["https://www.udemy.com"]
    cookies = None
    def parse(self, response):
        #Credenciales de inicio de sesión
        username = 'lizeth.avendano2870@alumnos.udg.mx'
        password = 'Monkeycursos8#'

        #Solicitud POST para iniciar sesión
        yield FormRequest(
            url='https://www.udemy.com/join/login-popup/',
            formdata={'email': username, 'password': password},
            callback=self.after_login,
            meta={'cookiejar': 1}
        )
    def start_requests(self):
        # Agrega un User-Agent a la solicitud similar al de Brave
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Brave/1.60.110'}
        yield scrapy.Request(url='https://www.udemy.com', headers=headers, callback=self.parse)

    def after_login(self, response):
        if "Bienvenido" in response.text:
            self.log('Inicio de sesión exitoso!')
            self.cookies = response.headers.getlist('Set-Cookie')
            # Continúa con la exploración después del inicio de sesión
            return scrapy.Request(url='https://www.udemy.com', callback=self.parse, cookies=self.cookies)
        else:
            self.log('Fallo en el inicio de sesión. Verifica tus credenciales.')

    def parse(self, response):
        course_links = response.css('.course-card--container a::attr(href)').extract()
        for course_link in course_links:
            yield scrapy.Request(url=course_link, callback=self.parse_course)

    def parse_course(self, response):

        course_title = response.css('.udlite-heading-xl::text').get()
        course_discount = response.css('.price-text--price-part--Tu6MH::text').get()


        self.log(f'Título del curso: {course_title}, Descuento: {course_discount}')

        yield {
            'title': course_title,
            'discount': course_discount,
        }
