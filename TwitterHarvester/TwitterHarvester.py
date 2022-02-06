from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from lxml import etree

import os
from time import sleep
from random import uniform, randint
from hashlib import md5
import json
import csv

TWITTER_URL = 'https://twitter.com'
TWITTER_LOGIN_URL = f'{TWITTER_URL}/i/flow/login'
TWITTER_USER_ELEMENT_XPATH = '//input[@autocomplete =\'username\']'
TWITTER_PASSWD_ELEMENT_XPATH = '//input[@autocomplete =\'current-password\']'
DOESNOT_EXIST_DIV_XPATH = '//div[@class = "css-901oao r-1fmj7o5 r-37j5jr r-1yjpyg1 r-1vr29t4 r-ueyrd6 r-5oul0u r-bcqeeo r-fdjqy7 r-qvutc0"]'
TWEET_ELEMENT_XPATH = '//article[@data-testid ="tweet"]'
TWEET_USER_HANDLE_RELEVANT_XPATH = './/span[contains(text(), "@")]'
TWEET_USER_NAME_RELEVANT_XPATH = './/span'
TWEET_RETWEETED_XPATH = './/*[@id="id__4yy3gbsml85"]'
TWEET_TIME_RELEVANT_XPATH = './/time'
TWEET_COMMENT_RELEVANT_XPATH = './/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span'
TWEET_RESPONDING_RELEVANT_XPATH = './/div[2]/div[2]/div[2]/div[2]'
TWEET_REPLYS_RELEVANT_XPATH = './/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[1]/div/div/div[2]/span/span/span'
TWEET_RETWEETS_RELEVANT_XPATH = './/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[2]/div/div/div[2]/span/span/span'
TWEET_LIKES_RELEVANT_XPATH = './/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div[2]/span/span/span'
TWITTER_NUMBER_OF_TWEETS_XPATH = '/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div[2]/div/div'

class Tweet:
    
    def __init__(self, tweet_etree_element):
        
        try:
            self.time = tweet_etree_element.xpath(TWEET_TIME_RELEVANT_XPATH)[0].get('datetime')
            self.is_sponsored = False
        except:
            self.is_sponsored = True
            return

        self.retweeted = False
        self.user_name = tweet_etree_element.xpath(TWEET_USER_NAME_RELEVANT_XPATH)[1].text
        self.user_handle = tweet_etree_element.xpath(TWEET_USER_HANDLE_RELEVANT_XPATH)[0].text
        
        if self.user_name is None:
            self.user_name = ''
            self.user_handle = ''
            self.retweeted = True
            
        try:
            self.comment = tweet_etree_element.xpath(TWEET_COMMENT_RELEVANT_XPATH)[0].text
        except IndexError:
            self.comment = 'No text in the tweet'
#         self.responding = tweet_etree_element.xpath(TWEET_RESPONDING_RELEVANT_XPATH).text
        self.replys = tweet_etree_element.xpath(TWEET_REPLYS_RELEVANT_XPATH)[0].text
        self.retweets = tweet_etree_element.xpath(TWEET_RETWEETS_RELEVANT_XPATH)[0].text
        self.likes = tweet_etree_element.xpath(TWEET_LIKES_RELEVANT_XPATH)[0].text
    
    def calc_hash(self):
        """:returns unique string for each tweet"""
        return md5((self.user_name + self.user_handle + self.comment + self.replys + self.retweets + self.likes).encode()).hexdigest()
    
    def to_dict(self):
        """converts tweet obj to json"""
        tweet = dict()
        if not self.is_sponsored:
            tweet['time'] = str(self.time)
        tweet['sponsored'] = str(self.is_sponsored)
        
        if not self.retweeted:
            tweet['user_name'] = self.user_name
            tweet['user_handle'] = self.user_handle
        
        tweet['retweeted'] = self.retweeted
        tweet['comment'] = self.comment
        tweet['replys'] = self.replys
        tweet['retweets'] = self.retweets
        tweet['likes'] = self.likes
        
        return tweet
        

class TwitterBot:

    user = None
    passwd = None
    CREDENTIALS = None
    LOGGED_IN = None
    soup = None

    def __init__(self, driver, user=None, passwd=None):

        self.driver = driver
        if user and passwd:
            self.set_login_credentials(user, passwd)

    def set_login_credentials(self, user, passwd):
        """Sets user and password credentials for the login process"""
        self.CREDENTIALS = True
        self.user = user
        self.passwd = passwd

    def login(self):
        """Login with provided credentials or cookies"""
        self.driver.get(TWITTER_LOGIN_URL)

        if self.CREDENTIALS:
            # wait until user element is available
            user_element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, TWITTER_USER_ELEMENT_XPATH)))

            # enter user credentials with human speed
            for i in range(len(self.user)):
                user_element.send_keys(self.user[i])
                # sleep in range 0.1 and 0.6
                sleep(round(uniform(.1,.6), 1))

            user_element.send_keys(Keys.RETURN)

            # wait until passwd element is available
            passwd_element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, TWITTER_PASSWD_ELEMENT_XPATH)))

            # enter password credentials with human speed
            for i in range(len(self.passwd)):
                passwd_element.send_keys(self.passwd[i])
                # sleep in range 0.1 and 0.4
                sleep(round(uniform(.1,.4), 1))

            passwd_element.send_keys(Keys.RETURN)

        return self.check_login()

    def check_login(self):
        """Check login process result"""
        sleep(3)
        if self.driver.current_url != TWITTER_LOGIN_URL:
            return True
        return False
    
    def collect_tweets_from_profile(self, username, n):
        """:returns list of n tweets or false if the username doesn't exist"""
        self.driver.get(TWITTER_URL + f'/{username}')

        valid_username = self.check_if_username_exists()
        
        if not valid_username:
            print('Error: Invalid username/handle')
            return False
        
        number_of_tweets = self.get_number_of_profile_tweets()
        
        if n > number_of_tweets:
            print(f'Error: Cant\'t scrape tweets more than the profile\'s tweets, setting n to {number_of_tweets}')
            n = number_of_tweets
        
        tweets = []
        tweets_hashes = []
        
        last_scroll_bar_position = self.get_current_scroll_bar_position()

        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, TWEET_ELEMENT_XPATH)))

        while len(tweets) < n:
            
            sleep(1)
            page_source_etree = etree.HTML(self.driver.page_source)
            tweets_elements = page_source_etree.xpath(TWEET_ELEMENT_XPATH)

            for tweet_element in tweets_elements:

                tweet = Tweet(tweet_element)
                
                if tweet not in tweets and not tweet.is_sponsored and not tweet.retweeted and tweet.calc_hash() not in tweets_hashes:
                    tweets.append(tweet)
                    tweets_hashes.append(tweet.calc_hash())

                    if len(tweets) == n:
                        break

            self.scroll_down(1000)
            if last_scroll_bar_position == self.get_current_scroll_bar_position():
                break

        return tweets

    def scroll_down(self, num):
        """executes JS code on the browser to scroll down"""
        self.driver.execute_script(f'window.scrollTo(0, window.scrollY + {num})')
        return self.get_current_scroll_bar_position()
    
    def get_current_scroll_bar_position(self):
        """executes JS code on the browser to get scroll bar position"""
        return self.driver.execute_script('return window.pageYOffset')
    
    def check_if_username_exists(self):
        """:returns true if the username exists, otherwise false"""
        try:
            number_of_tweets = WebDriverWait(self.driver, 3).until(ec.visibility_of_element_located((By.XPATH, DOESNOT_EXIST_DIV_XPATH)))
            return False
        except TimeoutException:
            return True
    
    def get_number_of_profile_tweets(self):
        """:returns number of tweets on the profile"""
        number_of_tweets = WebDriverWait(self.driver, 3).until(ec.visibility_of_element_located((By.XPATH, TWITTER_NUMBER_OF_TWEETS_XPATH))).text.split(' ')[0]
        if 'K' in number_of_tweets:
            number_of_tweets = number_of_tweets.replace('K', '')
            number_of_tweets = float(number_of_tweets)*1000

        return int(number_of_tweets)
    
    def save_as_json(self, filename, tweets_list):
        """save tweets list as JSON file"""
        tweets_json_list = list()
        
        for tweet in tweets_list:
            tweets_json_list.append(tweet.to_dict())

        tweets_json_list = json.dumps(tweets_json_list, indent=4)
        
        with open(filename, 'w') as j:
            j.writelines(tweets_json_list)

    def save_as_csv(self, filename, tweets_list):
        """save tweets list as CSV file"""
        tweets_dict_list = list()
        
        for tweet in tweets_list:
            tweets_dict_list.append(tweet.to_dict())

        tweet_details = tweets_dict_list[0].keys()

        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=tweet_details)
            writer.writeheader()
            writer.writerows(tweets_dict_list)


if __name__ == '__main__':
    
    driver = webdriver.Firefox()
    bot = TwitterBot(driver, user='', passwd='')
    tweets = bot.collect_tweets_from_profile('elonmusk', 10)
    bot.save_as_json('elonmusk-tweets.json', tweets)
    bot.save_as_csv('elonmusk-tweets.csv', tweets)
