import scrapy
import os
import PyPDF2
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
            file_path = os.path.join('pdfs', pdf_name)
            if not os.path.exists('pdfs'):
                os.makedirs('pdfs')
            yield scrapy.Request(url=pdf_url, meta={'file_path': file_path}, callback=self.save_pdf)

    def save_pdf(self, response):
        # Save the downloaded PDF to the static directory
        pdf_name = response.url.split('/')[-1]
        file_path = os.path.join(settings.STATICFILES_DIRS[0], 'pdfs', pdf_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)
        self.logger.info(f'Saved PDF to {file_path}')

        # Convert the PDF to a text file
        text_name = os.path.splitext(pdf_name)[0] + '.txt'
        text_path = os.path.join(settings.STATICFILES_DIRS[0], 'texts', text_name)
        with open(text_path, 'w') as f:
            pdf_reader = PyPDF2.PdfFileReader(open(file_path, 'rb'))
            for page_num in range(pdf_reader.getNumPages()):
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
                f.write(text)

        self.logger.info(f'Converted PDF to text file {text_path}')
