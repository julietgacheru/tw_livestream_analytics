# description:

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import numpy as np
import re


class TweetAnalyze:
    # convert to dataframe
    def __init__(self, positive=0, neutral=0, negative=0):
        self.positive_count = positive
        self.neutral_count = neutral
        self.negative_count = negative

    def tweets_dataframe(self, tweets_file):
        # load csv
        df = pd.read_csv(tweets_file, sep=",", usecols=["text"])
        # If column2 contains NaN, remove that row
        df.dropna(subset=["text"], inplace=True)
        df["text"] = [self.clean_tweet_text(tweet) for tweet in df["text"]]
        return df

    # clean
    def clean_tweet_text(self, tweet_text):
        # remove #, RT, hyperlinks
        return re.sub(r'(#)|(RT[\s]+)|(https?:\/\/\S+)', '', tweet_text)

    # word cloud

    def word_list(self, tweet_text):

        # Generate a word cloud image
        text = ""
        text += tweet_text
        return text

    def word_cloud(self, words, graph_name):
        text = ' '.join(words)
        stopwords = set(STOPWORDS)

        # stopwords.update(["joe","Biden","Trump","vladimir"])

        wordcloud = WordCloud(
            stopwords=stopwords,
            width=1600,
            height=1000,
            max_words=100,
            background_color="black",
            max_font_size=200,
            colormap="Set2",
            collocations=False).generate(text)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        wordcloud.to_file(graph_name)

    # sentiment analysis
    def sentiment_tweet_vader(self, tweet_text):
        sid = SentimentIntensityAnalyzer()
        # Generate sentiment scores
        sentiment_scores = sid.polarity_scores(tweet_text)
        if sentiment_scores["compound"] > 0.6:
            self.positive_count += 1
            return 1
        elif sentiment_scores["compound"] < -0.6:
            self.negative_count += 1
            return -1
        else:
            self.neutral_count += 1
            return 0

        return sentiment_scores

    def sentiment_plot(self, df_tweets, graph_name):
        fg, ax = plt.subplots(figsize=(8, 6))
        # Plot histogram of the polarity values
        df_tweets.hist(bins=[-1, -0.75, -0.5, -0.25, 0.25,
                             0.5, 0.75, 1], ax=ax, color="#1DA1F2")
        plt.xlabel(
            "Negative                  Neutral                   Positive",
            fontsize=15)
        plt.ylabel("#Tweets", fontsize=15)
        plt.title("Sentiments from Tweets")
        fg.savefig(graph_name, dpi=200)


if __name__ == '__main__':
    main()
