## Twitter Stream Analytics [word cloud and sentiment analysis] GUI

### Description

Twitter Stream Analytics [word cloud and sentiment analysis] GUI is a python GUI app that collects tweets from the Twitter Streaming API using Python based on user-specific hashtag, topic or twitter handle and stores them in CSV format. A Tkinter GUI displays live tweets and also displays a Texblob and a simple graph of sentimental analysis of the collected tweets using Vader. 

### Dependencies 

Refer to requirements.txt 

### Installation 

##### Method 1 

```bash
pip install -r requirements.txt
```

##### Method 2

```bash
pip install tweepy
pip install vaderSentiment
pip install wordcloud
pip install matplotlib
pip install pandas
```
### Generate Twitter Credentials
Create a Twitter account if you do not have one. From https://apps.twitter.com/ and “Create a New App.

From the Keys and tokens menu in your created app, copy the following 

Consumer API keys
	- API key = CONSUMER_KEY 
	- API secret key = CONSUMER_SECRET
Access token & access token secret
	- Access token = ACCESS_TOKEN
	- Access token secret = ACCESS_TOKEN_SECRET

### License
[MIT](https://choosealicense.com/licenses/mit/)