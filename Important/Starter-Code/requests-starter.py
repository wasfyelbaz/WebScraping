import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.amazon.com/dp/B08F8HKQ4B?ref=ods_ucc_kindle_B08F8HKQ4B_nrc_ucc"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"

headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': USER_AGENT,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

page = requests.get(url, headers=headers)
print(page.status_code)
