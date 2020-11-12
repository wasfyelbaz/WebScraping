"""
This script is based on "https://www.autoscout24.com" and there is no illegal actions towards this
great company and there is no rule that disallows web crawlers or spiders on this website.
"""
import Extractor
import Formator
import requests
from bs4 import BeautifulSoup
import json
from time import sleep

CARS_MANUFACTURER_JSON = "manufacturer.json"
CARS_LIST = []
BASE_URL = "https://www.autoscout24.com"
PAGE = 1
ex = Extractor.ExtractCars()
fr = Formator.FormatResults()

MANUFACTURER = input("* Manufacturer: ")


def find_manufacturer(manufacturer):

    with open(CARS_MANUFACTURER_JSON, "r") as f:
        cmj = json.load(f)

    for m in cmj:

        if manufacturer.upper() in m["label"].upper():
            print(f"  + Found {m['label']}")
            return m["label"]

    return "Unknown"


MANUFACTURER = find_manufacturer(MANUFACTURER)
RESULTS_NAME = f"res-{MANUFACTURER}"
fr.results_file_name = RESULTS_NAME

MODEL = input("* MODEL (Leave Empty for all models): ")
if MODEL == "":
    print("  + Selected all models")

PRICE_TO = input("* Max-Price (Leave Empty for all prices): ")
if PRICE_TO == "":
    print("  + All prices are allowed")

YEAR = input("* Model-Year (Leave Empty for all years): ")
if YEAR == "":
    print("  + All years are allowed")

SAVE_MODE = int(input("* Save as:\n\n  (1) JSON File Only\n  (2) HTML File and JSON\n>> "))


def extract_cars_from_url(url):

    sleep(1)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    ex.source_code = soup
    ex.base_url = BASE_URL
    ex.run()

    return ex.cars_list


PATH = ""

for i in range(1, 21):

    PATH = f"/lst/{MANUFACTURER}/{MODEL}?sort=standard&desc=0&ustate=N%2CU&size=20&page={PAGE}&priceto={PRICE_TO}&fregfrom={YEAR}&atype=C&"
    FULL_URL = BASE_URL + PATH
    print(f"* Getting data from page {PAGE}")
    print(FULL_URL)

    for car in extract_cars_from_url(FULL_URL):
        CARS_LIST.append(car)

    PAGE += 1

if SAVE_MODE == 1:
    fr.create_json_file(CARS_LIST)
elif SAVE_MODE == 2:
    fr.create_html_js_result_file(CARS_LIST)
