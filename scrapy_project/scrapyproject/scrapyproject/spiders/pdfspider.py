import scrapy
import os
import io
import pdfplumber
from django.conf import settings


class PDFSpider(scrapy.Spider):
    name = 'pdf_spider'
    start_urls = []

    def __init__(self, start_url=None, *args, **kwargs):
        super(PDFSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        
    def parse(self, response):
        # Extract data from the main page if needed
        title = response.css('.table-td-c-t::text').extract()
        download_link = response.css('.col-md-2 a:nth-child(1)::attr(href)').extract()

        for i in range(len(title)):
            data = {}
            data['rule_name'] = [title[i].strip()]
            data['pdf_link'] = [download_link[i+2]]
            yield data

            # Download the PDF for this rule
            pdf_url = data['pdf_link'][0]
            pdf_name = data['rule_name'][0] + '.pdf'
            if not os.path.exists('pdfs'):
                os.makedirs('pdfs')
            yield scrapy.Request(url=pdf_url, meta={'pdf_name': pdf_name}, callback=self.save_pdf)

    def save_pdf(self, response):
        # Convert the PDF to a text file
        pdf_bytes = response.body
        pdf_name = response.meta['pdf_name']
        text_name = os.path.splitext(pdf_name)[0] + '.txt'
        text_path = os.path.join(settings.STATICFILES_DIRS[0], 'pdfs', text_name)
        with open(text_path, 'w') as f:
            with io.BytesIO(pdf_bytes) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        f.write(text)

        self.logger.info(f'Converted PDF to text file {text_path}')
