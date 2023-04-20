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
            pdf_folder = os.path.join(settings.DOWNLOADS_FOLDER, 'pdfs')
            pdf_path = os.path.join(pdf_folder, pdf_name)
            if not os.path.exists(pdf_folder):
                os.makedirs(pdf_folder)
            yield scrapy.Request(url=pdf_url, meta={'pdf_path': pdf_path}, callback=self.save_pdf)

    def save_pdf(self, response):
        # Convert the PDF to a text file
        pdf_bytes = response.body
        pdf_path = response.meta['pdf_path']
        text_name = os.path.splitext(os.path.basename(pdf_path))[0] + '.txt'
        text_path = os.path.join(settings.DOWNLOADS_FOLDER, 'pdfs', text_name)
        with open(text_path, 'w') as f:
            with io.BytesIO(pdf_bytes) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        f.write(text)

        self.logger.info(f'Converted PDF to text file {text_path}')
