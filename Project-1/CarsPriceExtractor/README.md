#**Cars Price Extractor**
![alt text](https://i.ibb.co/ZKbJ5L4/logo-removebg-preview.png "Cars Price Extractor")

## Note
* #### This script is based on [autoscout24.com](https://www.autoscout24.com) where script user can extract data about a number of cars based on car
    * Manufacturer
    * Model
    * Price Range
    * Model Year
* #### Prices are only in euro (€)
* #### Cars you find are only in europe
## Dependencies
* python3
* python3 modules
    - requests
    - bs4
    
## Installation

    git clone https://github.com/wasfyelbaz/WebScraping.git
    
    if windows:
        cd Project-1\CarsPriceExtractor
    elif linux:
        cd Project-1/CarsPriceExtractor
        
    pip3 install -r requirements.txt

## Usage

* Edit settings.json file.
    * change {target_username} to your target's username
    * change the {number_of_tweets} to match your needs
```json
    {
        "target_username": "TestForScrapper", # Target User
        "number_of_tweets": 10 # Number of tweets to be crawled
    }
```
* Then execute:
```bash
python3 Main.py
```

## Results
* After the script finish executing the result will be saved in a JSON file and can be displayed in html file either.
    * Example JSON Result for a car:
```json
    {
            "name": car_name,
            "price": car_price,
            "mileage": car_mileage,
            "transmission": car_transmission,
            "offer_type": car_offer_type,
            "previous_owners": car_previous_owners,
            "first_registration": car_first_registration,
            "link": self.base_url + car_link
    }
```
* #### Which is:
    * ##### Car name (Title)
    * ##### Car price
    * ##### car millage
    * ##### Car transmission type
    * ##### Car offer type (Used/New)
    * ##### Car previous owners
    * ##### Car first registration date
    * ##### Car link on [autoscout24.com](https://www.autoscout24.com)

* Check the "ExampleResult" dir to see an example of a json-result file.
