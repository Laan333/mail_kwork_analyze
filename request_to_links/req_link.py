import re
import asyncio
from playwright.sync_api import sync_playwright

async def link_parser(link: str) -> list[str]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sync_scraper, link)

def sync_scraper(link: str) -> list[str]:
    """Синхронный парсер в отдельном потоке"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link)
        page.wait_for_load_state('networkidle')
        page.wait_for_selector('.wants-card__header-title')

        title_elem = page.query_selector('.wants-card__header-title')
        text_elem = page.query_selector('.wants-card__description-text')
        price_elem = page.query_selector('.wants-card__price')
        high_price_elem = page.query_selector('.wants-card__description-higher-price')

        title = title_elem.text_content() if title_elem else "Название не найдено"
        text = text_elem.text_content() if text_elem else "Описание отсутствует"
        price = price_elem.text_content() if price_elem else "0Р"
        high_price = high_price_elem.text_content() if high_price_elem else "0P"

        price = re.sub(r'\D', "", price) + 'Р'
        high_price = re.sub(r'\D', "", high_price) + "P"

        browser.close()
        return [title, text, price, high_price]