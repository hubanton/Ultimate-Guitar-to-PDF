import os.path

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, Edge, Firefox, ChromeOptions, EdgeOptions, FirefoxOptions
from selenium.common.exceptions import WebDriverException
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import urlparse, urljoin


def init_selenium():
    webdriver = None

    driver_options = {
        Chrome: ChromeOptions,
        Firefox: FirefoxOptions,
        Edge: EdgeOptions,
    }

    for driver_class, options_class in driver_options.items():
        try:
            options = options_class()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            webdriver = driver_class(options=options)
            break
        except WebDriverException as e:
            print(f'Error initializing {webdriver.name}: {e}')
            continue

    if webdriver:
        print(f'Successfully initialized {webdriver.name}')
    else:
        Exception('Could not find any valid webdriver')

    return webdriver
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

def convert_to_pdf(filename, text):
    font = "Courier"
    fontSize = 10

    pdf_canvas = canvas.Canvas(os.path.join('output', filename + '.pdf'), pagesize=letter)
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
