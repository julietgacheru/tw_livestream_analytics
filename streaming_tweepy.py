# description: collect tweets from the Twitter Streaming API

from tweepy import StreamListener, Stream, OAuthHandler, API
from tkinter import END
from csv import DictWriter
from datetime import date
import json
import os
import logging
import sys
import credentials


# listener class inheriting from StreamListener
class MyStreamListener(StreamListener):

    tweet_counter = 0

    def __init__(self, fetched_tweets_file, tweet_list):

        file_header = (
            "length",
            "id_str",
            "created_at",
            "text",
            "screen_name",
            "location",
            "followers_count",
            "quoted_text")

        self.tweet_list = tweet_list
        self.file_exists = os.path.isfile(fetched_tweets_file)
        self.headers = file_header
        self.file = open(fetched_tweets_file, "w", encoding="UTF-8")
        self.csv_writer = DictWriter(self.file, fieldnames=self.headers)

        if not self.file_exists:
            self.csv_writer.writeheader()

    def on_data(self, data):

        MyStreamListener.tweet_counter += 1
        try:
            is_retweet = False
            is_quote = False
            quote = ""
            char_remove = [",", "\n"]
            # convert from JSON to Python object
            tweet = json.loads(data)

            text = ""
            # check if truncated
            if "extended_tweet" in tweet:

                if hasattr(tweet, "extended_tweet"):
                    text = tweet["extended_tweet"]["full_text"]

                else:

                    text = tweet["text"]

            #  if retweeted

            if "retweeted_status" in tweet:
                is_retweet = True

                if hasattr(tweet["retweeted_status"], "extended_tweet"):
                    text = tweet["retweeted_status"]["extended_tweet"]["full_text"]
                else:

                    text = tweet["retweeted_status"]["text"]

            # is tweet quoted

            if "quoted_status" in tweet:
                is_quote = True
                if "extended_tweet" in tweet["quoted_status"]:

                    text = tweet["quoted_status"]["extended_tweet"]["full_text"]
                else:
                    text = tweet["quoted_status"]["text"]
            text.replace('\n', '')

            self.csv_writer.writerow({
                "length": len(tweet["text"]),
                "id_str": tweet["id_str"],
                "created_at": tweet["created_at"],
                "text": text,
                "screen_name": tweet["user"]["screen_name"],
                "location": tweet["user"]["location"],
                "followers_count": tweet["user"]["followers_count"],
                "quoted_text": is_quote
            })
            self.tweet_list.insert(
                1, str(MyStreamListener.tweet_counter) + "....." + text)

        except BaseException as e:
            logging.exception(str(e))

        if MyStreamListener.tweet_counter >= 1000:
            sys.exit('Limit of ' + str(1000) + ' tweets reached.')

        return True

    def on_error(self, status_code):

        if status_code == 420:
            # return False in on_error disconnects the stream
            return False


class TweetStreamer:
    """ class for streaming live tweets"""

    def stream_tweets(self, fetched_tweets_file, filter_topic, tweet_list):

        # authorize and initialize API endpoint
        auth = OAuthHandler(
            credentials.CONSUMER_KEY,
            credentials.CONSUMER_SECRET)
        auth.set_access_token(
            credentials.ACCESS_TOKEN,
            credentials.ACCESS_TOKEN_SECRET)
        # Set up the API with the authentication handler

        api = API(auth)

        # initialize a stream
        myListener = MyStreamListener(fetched_tweets_file, tweet_list)
        # create twitter stream
        myStream = Stream(
            auth=auth,
            listener=myListener,
            tweet_mode="extended")

        myStream.filter(track=filter_topic)


if __name__ == '__main__':

    # initialize the log settings
    logging.basicConfig(filename='app.log', level=logging.INFO)
