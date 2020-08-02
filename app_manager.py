# description:

from tkinter import Tk, Label, Button, StringVar, Entry, Listbox, Scrollbar, END
from datetime import date
import threading
import streaming_tweepy
import sentiment_wordcloud
from PIL import ImageTk, Image
import os

# sentiment_analysis.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import numpy as np
import re


class AppGUI:
    def __init__(self, master):
        self.master = master
        master.title("Twitter Streaming")
        master.geometry("950x750")
        master.resizable(0, 0)
        self.create_widgets()
        self.filename = ""
        self.filter_topic = []
        self.graph_name = ""

    def create_widgets(self):
        #  Label
        self.num_label = Label(
            self.master,
            text="Collect Twitter Live Streaming Tweets",
            font=(
                "bold",
                16),
            padx=20,
            pady=20,
            fg="#1DA1F2")
        self.num_label.grid(row=0, column=1, sticky="W")

        # keywords
        self.key_text = StringVar()
        self.key_label = Label(
            self.master, text="Keyword", font=(
                "bold", 16), padx=20, pady=20, fg="#1DA1F2")
        self.key_label.grid(row=1, column=0, sticky="W")
        self.key_entry = Entry(self.master, textvariable=self.key_text)
        self.key_entry.grid(row=1, column=1)
        self.submit_key = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="ENTER",
            width=5,
            height=2,
            padx=20,
            command=self.add_keywords)
        self.submit_key.grid(row=1, column=2)
        # output file
        self.ofile_text = StringVar()
        self.ofile_label = Label(
            self.master, text="Output File", font=(
                "bold", 16), padx=20, pady=20, fg="#1DA1F2")
        self.ofile_label.grid(row=2, column=0, sticky="W")
        self.ofile_entry = Entry(self.master, textvariable=self.ofile_text)
        self.ofile_entry.grid(row=2, column=1)
        self.submit_ofile = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="SUBMIT",
            width=5,
            height=2,
            padx=20,
            command=self.add_outputfile)
        self.submit_ofile.grid(row=2, column=2)
        # start tweet streaming
        self.submit_ofile = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="START STREAMING",
            width=16,
            height=3,
            command=self.start_streaming)
        self.submit_ofile.grid(row=3, column=1, pady=20)

        # close

        self.close_button = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="STOP",
            width=5,
            height=2,
            padx=20,
            command=self.close_program)
        self.close_button.grid(row=3, column=2, pady=20)

        # Tweet streaming (Listbox)
        self.tweet_list = Listbox(self.master, height=10, width=50, border=0)
        self.tweet_list.grid(
            row=4,
            column=0,
            columnspan=4,
            rowspan=8,
            pady=20,
            padx=20)

        # Create scrollbar
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.grid(row=4, rowspan=8, column=3)

        # Set scroll to listbox
        self.tweet_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.tweet_list.yview)

        #  Label
        self.num_label = Label(
            self.master,
            text="WordCloud and Sentimental Analysis",
            font=(
                "bold",
                16),
            padx=20,
            pady=20,
            fg="#1DA1F2")
        self.num_label.grid(row=0, column=7, sticky="W")

        # graphs
        self.submit_graphn = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="Sentiment Analysis",
            width=10,
            height=2,
            padx=20,
            command=self.display_sentgraph)
        self.submit_graphn.grid(row=1, column=6, columnspan=3)

        self.submit_wordcloud = Button(
            self.master,
            highlightbackground="#1DA1F2",
            bg="#1DA1F2",
            text="WordCloud",
            width=10,
            height=2,
            padx=20,
            command=self.display_wordcloud)
        self.submit_wordcloud.grid(row=2, column=6, columnspan=3)

    # add keyworks
    def add_keywords(self):
        ele = self.key_entry.get()
        self.filter_topic.append(ele)
        self.key_entry.delete(0, 'end')

    # add output file
    def add_outputfile(self):
        ele = self.ofile_entry.get()
        self.filename = str(date.today()) + "-" + \
            ele.replace(" ", "-") + ".csv"

    def close_program(self):
        self.master.quit()

    def init_streaming(_, filename, filter_topic, tweet_list):
        tweepy_streamer = streaming_tweepy.TweetStreamer()
        tweepy_streamer.stream_tweets(filename, filter_topic, tweet_list)

    # start streaming
    def start_streaming(self):
        self.streaming_thread = threading.Thread(
            target=self.init_streaming, args=(
                self.filename, self.filter_topic, self.tweet_list))
        self.streaming_thread.daemon = True
        self.streaming_thread.start()
        self.tweet_list.insert(
            1, ("FILTER TOPIC : " + ",".join(self.filter_topic)))

    def display_sentgraph(self):
        tweets_file = self.filename
        self.graph_name = tweets_file.replace('.csv', '.png')
        tweet_analyze_vader = sentiment_analysis.TweetAnalyze()

        # df.to_csv('/Users/juliet/Desktop/julietgacheru/project/dev/tweepy_twitter/sentiment_analysis/file1.csv')

        # tweet dataframe
        df = tweet_analyze_vader.tweets_dataframe(tweets_file)

        # sentimental analysis graph

        df["sentiment"] = np.array(
            [tweet_analyze_vader.sentiment_tweet_vader(tweet)for tweet in df["text"]])
        tweet_analyze_vader.sentiment_plot(df, self.graph_name)

        # Creates a Tkinter-compatible photo image
        self.img = ImageTk.PhotoImage(
            Image.open(
                self.graph_name).resize(
                (400, 400), Image.ANTIALIAS))

        # The Label widget i
        self.panel = Label(self.master, image=self.img)
        self.panel.grid(row=4, column=6, columnspan=3, pady=20)

    def display_wordcloud(self):
        tweets_file = self.filename
        self.graph_name = tweets_file.replace('.csv', '.png')
        tweet_analyze_vader = sentiment_analysis.TweetAnalyze()

        # tweet dataframe
        df = tweet_analyze_vader.tweets_dataframe(tweets_file)

        # wordcloud
        words_list = [tweet_analyze_vader.word_list(
            tweet) for tweet in df["text"]]
        tweet_analyze_vader.word_cloud(words_list, self.graph_name)

        self.img = ImageTk.PhotoImage(
            Image.open(
                self.graph_name).resize(
                (360, 360), Image.ANTIALIAS))

        self.panel = Label(self.master, image=self.img)
        self.panel.grid(row=4, column=7, pady=20)


if __name__ == '__main__':
    root = Tk()
    my_gui = AppGUI(root)
    root.mainloop()
