import sys
import pyfiglet
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright

from rich.console import Console
from rich.text import Text

url = 'https://forum.valuepickr.com/'

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = url


def printf_underline(str):
    for char in str:
      print(char + "\u0332", end='')
    print()


async def load_entire_page(page):
    previous_height = None
    while True:
        # Scroll down to the bottom of the page
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        await asyncio.sleep(2)  # Wait for new content to load

        # Calculate new scroll height and compare with previous height
        new_height = await page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        #await page.goto('https://chartink.com/screener/on-balance-volume-sloping-2-days-in-nifty-200')
        await page.goto(url)
        content = await page.content()
        #print(content)
        await browser.close()
        return content


async def read_post_threads(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)


        # Ensure the entire page content is loaded
        await load_entire_page(page)

        content = await page.content()

        # Select all article elements
        articles = await page.query_selector_all('article')


        # Get the last two articles
        last_two_articles = articles[-2:]

        # Loop through the last two articles and extract paragraphs
        for article in last_two_articles:
            # Get the article ID
            article_id = await article.get_attribute("id")
            # Get paragraphs within the article
            paragraphs = await article.query_selector_all('p')
            #print(f'Paragraphs under {article_id}:')
            printf_underline(f'Paragraphs under {article_id}:')
            for p in paragraphs:
                text = await p.inner_text()
                print(text)
            print()

        await browser.close()
        return content






content = asyncio.run(run())

exclude_headline_list = [ 'faq-guidelines', 'stock_valuepickr_healine' , 'welcome-to-valuepickr-investing-forums' ]

# Parse the HTML
soup = BeautifulSoup(content, 'html.parser')

post_activity_links = soup.find_all('a', class_='post-activity')

# Extract and print the href attribute of each matching tag
for link in post_activity_links:
    href = link.get('href')
    if href:
        tokens = href.split('/')
        if len(tokens) > 2:
            stock_valuepickr_healine = tokens[2]
            if stock_valuepickr_healine in exclude_headline_list:
                continue

            #print(stock_valuepickr_healine)
            #print(pyfiglet.Figlet(font='slant').renderText(stock_valuepickr_healine))
            text = Text(stock_valuepickr_healine, style="bold underline")
            text.stylize("font-family:Menlo", 0, len(text))
            text.stylize("size=44", 0, len(text))
            Console().print(text)
            print()
            page_link = "https://forum.valuepickr.com" + href.rsplit('/',1)[0]
            content = asyncio.run(read_post_threads(page_link))
