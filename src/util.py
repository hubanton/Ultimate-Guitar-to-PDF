from bs4 import BeautifulSoup
from selenium import webdriver
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import urlparse, urljoin


def init_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    return webdriver.Chrome(options=options)

def fetch_html(url):
    driver = init_selenium()
    driver.get(url)
    driver.implicitly_wait(10)
    webpage = driver.page_source
    driver.quit()
    return webpage
def get_meta_pre(all_spans):
    text = ''
    for span in all_spans:
        if span.find('span') != None:
            break
        text += span.text
    text += '\n'
    return text

def get_meta_post(all_spans):
    last_tab_index = 0
    text = ''

    for index, span in enumerate(all_spans):
        if span.find('span') != None:
            last_tab_index = index

    redundant_tabs = len(all_spans[last_tab_index].findAll('span'))

    for meta_info in all_spans[last_tab_index + 1 + redundant_tabs:]:
        text += meta_info.text
    return text

def extract_tabs(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')

    pre = soup.find('pre')

    return pre.text

def convert_to_pdf(text):
    font = "Courier"
    fontSize = 10

    pdf_canvas = canvas.Canvas('tabs.pdf', pagesize=letter)
    pdf_width, pdf_height = letter

    pdf_canvas.setFont(font, fontSize)

    x, y = 50, pdf_height - 20

    for tab in text.split('\n'):
        if y < 200 and tab == f'{chr(32)}{chr(13)}':
            pdf_canvas.showPage()
            pdf_canvas.setFont(font, fontSize)
            y = pdf_height - 20

        pdf_canvas.drawString(x, y, tab.strip())
        y -= 12

    pdf_canvas.save()

def get_full_url(tab_identifier):
    base_url = 'https://tabs.ultimate-guitar.com/tab/'
    # Check if the input is a complete URL
    if urlparse(tab_identifier).scheme:
        return tab_identifier
    else:
        # Assume it's the part after /tab/
        return urljoin(base_url, tab_identifier)
