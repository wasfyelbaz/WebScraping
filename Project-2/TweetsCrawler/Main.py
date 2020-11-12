import config
import TwitterHandle
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
from time import sleep
from pyvirtualdisplay import Display

with open(config.SETTINGS_JSON, "r") as f:
    cmj = json.load(f)

target_username = cmj["target_username"]
number_of_tweets = cmj["number_of_tweets"]


def create_json_file(data):

    data = json.dumps(data, indent=4)

    with open(f'{target_username}-{number_of_tweets}-tweets.json', "w") as f:
        f.write(data)


def start():

    # login_status = ta.login(username, passwd)
    # print(login_status)

    tweets_number = twitterActions.get_tweets_number()
    if tweets_number >= number_of_tweets:
        sleep(1)
        while len(twitterActions.tweets) < number_of_tweets:
            twitterActions.get_tweets_elements()
            twitterActions.scroll_down(500)
        driver.close()
    else:
        exit(f"[*] Can't get latest {number_of_tweets} tweets while \"{target_username}\" has only {tweets_number} tweets !")


twitterActions = TwitterHandle.TwitterActions()

try:
    driver = webdriver.Firefox()
except selenium.common.exceptions.WebDriverException:
    exit("Couldn't find geckodriver:\nPlease download it from https://github.com/mozilla/geckodriver/releases and add it to your PATH.")

driver.minimize_window()
twitterActions.driver = driver

twitterActions.target_username = target_username
twitterActions.number_of_tweets = number_of_tweets

print(f"[*] Going to {config.TWITTER_URL}{target_username}")
twitterActions.go_to_profile(target_username)

print(f"[*] Checking if user \"{target_username}\" exists !")
if twitterActions.is_existed() is True:
    print(f"[*] {target_username} exists, starting ..")
    start()
    print(f"[*] Creating JSON Results file \"{target_username}-{number_of_tweets}-tweets.json\"")
else:
    exit("[*] Wrong Username")

create_json_file(twitterActions.tweets)
