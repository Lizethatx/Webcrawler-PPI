# En MaliciousDetector/spiders/malicious_spider.py

import scrapy
import re

malicious_patterns = [
    r'malicious_function\(',
    r'<script>\s*eval\(',
    r'\bunion\s+select\b',
    r'\bexec\s*\(',
    r'\bselect\s*[\w\*]+\s*from\s*[\w]+\s*',
    r'<script\s*>\s*alert\(',
    r'<script\s*>.*eval\(',
    r'onerror\s*=\s*function\b',
    r'meta\s+http-equiv=["\']?refresh["\']?\s+content=["\']?\d+;\s*url=',
    r'window\.location\.replace\(',
    r'\b\.exe\b',
    r'\b\.dll\b',
    r'\\b(\\.\\./|\\./|/\\.\\./|/\\./|\\?\\./|\\?\\.\\./)\\b',  # Posible intento de navegación fuera de ruta
    r'\\b(?:\d{1,3}\.){3}\d{1,3}\\b',  # Posible dirección IP
    # Agrega más patrones según sea necesario
    ]

class MaliciousSpider(scrapy.Spider):
    name = 'malicious_spider'

    start_urls = ['http://example.com']  # Cambia esto con la URL de la página a analizar

    def contains_malicious_code(content):
        for pattern in malicious_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def parse(self, response):
        content = response.text
        if contains_malicious_code(content):
            self.log(f"Posible código malicioso encontrado en {response.url}")
        print(response.text)
        

    