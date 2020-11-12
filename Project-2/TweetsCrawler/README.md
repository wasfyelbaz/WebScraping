# Note
* A python3-based script for crawling a number of tweets from a specific user, End .. 
# Dependencies
* python3
* python3 modules
    - selenium
    - bs4
    - dateparser - in the future update
    
* [geckodriver](https://github.com/mozilla/geckodriver/releases)

# Installation

    git clone https://github.com/wasfyelbaz/WebScraping.git
    
    if windows:
        cd Project-2\TweetsCrawler
    elif linux:
        cd Project-2/TweetsCrawler
        
    pip3 install -r requirements.txt

# Usage

* Edit settings.json file.
    * change {target_username} to your target's username
    * change the {number_of_tweets} to match your needs
```json
    {
        "target_username": "TestForScrapper",
        "number_of_tweets": 10
    }
```
* Then execute:
```bash
python3 Main.py
```

# Results
* After the script finish executing it will save the tweets in a JSON file
    * Example:
```json
[
    {
        "string": "Tweet number - 10 {end !}",
        "time": "2020-11-12T10:44:54.000Z",
        "id": 0,
        "status": "Wrote"
    }
]
```
* Check the "ExampleResult" dir to see an example of a json-result file.
