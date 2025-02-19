import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re

def link_parser(link:str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(link)
        page.wait_for_selector('.want-card')
        title = page.query_selector('.wants-card__header-title')
        title = title.text_content()
        text = page.query_selector('.wants-card__description-text').text_content()
        price = page.query_selector('.wants-card__price').text_content()
        high_price = page.query_selector('.wants-card__description-higher-price').text_content()
        high_price = re.sub(r'\D', "", high_price) + "P"
        price = re.sub(r'\D', "", price) + 'Р'
        browser.close()
        return [title, text, price, high_price]
