import config
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
# import dateparser


class TwitterActions:

    driver = None
    tweets = []
    tweets_strings = []
    target_username = None
    number_of_tweets = None

    def __int__(self):
        pass

    # def login(self, login_username, login_password):
    #
    #     self.driver.get(config.TWITTER_LOGIN_URL)
    #
    #     username_field = self.driver.find_element_by_name(config.TWITTER_USERNAME_FIELD)
    #     passwd_field = self.driver.find_element_by_name(config.TWITTER_PASSWD_FIELD)
    #
    #     username_field.clear()
    #     username_field.send_keys(login_username)
    #
    #     sleep(1)
    #
    #     passwd_field.clear()
    #     passwd_field.send_keys(login_password)
    #
    #     sleep(1)
    #
    #     passwd_field.send_keys(Keys.RETURN)
    #     sleep(3)
    #
    #     if str(self.driver.current_url) == config.TWITTER_URL + "home":
    #         return True
    #     return False

    def go_to_profile(self, target):

        self.driver.get(config.TWITTER_URL + target)
        sleep(2)

    def is_existed(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        div_element = soup.find("div", {"class": config.NOT_EXISTED_DIV_CLASS})

        if div_element is None:
            return True
        elif div_element.text == "This account doesn’t exist":
            return False
        return True

    def scroll_down(self, num):
        self.driver.execute_script(f"window.scrollTo(0, window.scrollY + {num})")

    def get_tweets_number(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        div_elements = soup.find_all("div", {"class": config.TWEETS_NUMBER_CSS_CLASS})
        try:
            tweets_element = div_elements[config.TWEETS_NUMBER_ELEMENT]
        except IndexError:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            div_elements = soup.find_all("div", {"class": config.TWEETS_NUMBER_CSS_CLASS})
            tweets_element = div_elements[config.TWEETS_NUMBER_ELEMENT]

        tweets_number = tweets_element.text
        tweets_number = tweets_number.replace(" Tweets", "")

        if "K" in tweets_number:
            tweets_number = tweets_number.replace("K", "")
            tweets_number = tweets_number.replace(".", "")
            tweets_number = int(tweets_number)*100

        elif "," in tweets_number:
            tweets_number = tweets_number.replace(",", "")

        return int(tweets_number)

    def get_tweet_string(self, src_code):

        small_soup = BeautifulSoup(src_code, "html.parser")
        string = small_soup.find("div", {"class", config.TWEET_STRING_CLASS})
        try:
            string = string.text
        except:
            pass
        return string

    def get_tweet_time(self, src_code):

        small_soup = BeautifulSoup(src_code, "html.parser")
        # datetime.fromrfcformat()
        return small_soup.find("time")["datetime"]

    def get_tweet_id(self, src_code):

        small_soup = BeautifulSoup(src_code, "html.parser")
        a_elements = small_soup.find_all("a", {"class", config.TWEET_ID_ELEMENT_CLASS})
        for a_element in a_elements:
            try:
                element_href = a_element["href"]
                element_href = element_href.split("/")
                id = element_href[3]
                return id
            except:
                pass
        return 0

    def get_tweet_status(self, src_code):

        soup = BeautifulSoup(src_code, "html.parser")
        span_elements = soup.find_all("span", {"class", config.TWEETED_USER_SPAN_CLASS})

        if span_elements is not None:

            for span_element in span_elements:

                if "@" + self.target_username in span_element:
                    status = "Wrote"
                    return status

        return "Retweeted"

    def create_tweet(self, tweet_string, tweet_time, tweet_id, tweet_status):

        tweet = {
            "string": tweet_string,
            "time": tweet_time,
            "id": tweet_id,
            "status": tweet_status
        }
        return tweet

    def get_tweets_elements(self):

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        div_elements = soup.find_all("div")

        for element in div_elements:

            element = str(element)

            if "<div style=\"position: absolute; width: 100%;" in element:

                tweet_string = self.get_tweet_string(element)

                if tweet_string not in self.tweets_strings and tweet_string is not None and len(self.tweets) < self.number_of_tweets:

                    self.tweets_strings.append(tweet_string)
                    tweet_time = self.get_tweet_time(element)
                    tweet_id = self.get_tweet_id(element)
                    tweet_status = self.get_tweet_status(element)
                    tweet = self.create_tweet(tweet_string, tweet_time, tweet_id, tweet_status)

                    if len(self.tweets) < self.number_of_tweets:
                        self.tweets.append(tweet)

                    print(tweet)
                    self.scroll_down(60)
