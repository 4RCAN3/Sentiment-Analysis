# import required libraries
try:
    import tweepy
    from dotenv import load_dotenv
    import os
    from nltk.sentiment import SentimentIntensityAnalyzer
    import matplotlib.pyplot as plt
    import sys
    import csv
    from urllib3.exceptions import ProtocolError
    from urllib3 import exceptions as ec
except Exception as e:
    print("Error!")
    print(e)


class Twitter():

    def __init__(self) -> None:

        load_dotenv()
        api_key, api_secret = os.environ.get(
            'API_KEY'), os.environ.get('API_SECRET_KEY')
        access_token, access_token_secret = os.environ.get(
            'ACCESS_TOKEN'), os.environ.get('ACCESS_TOKEN_SECRET')

        # Auth
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Setting the API attribute for the class
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

        if self.api.verify_credentials():
            pass
        else:
            sys.exit('Authentication Error')

    def analyse(self, text):
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)

        return scores['compound']*10

    def historical(self, keyword, startDate, language='en'):
        api = self.api

        tweets = tweepy.Cursor(api.search, q=keyword,
                               lang=language, since=startDate, tweet_mode="extended").items()

        toPlot = {}
        for tweet in tweets:
            # Analyse tweet
            toPlot[tweet.created_at] = self.analyse(
                tweet.full_text)  # (Positivity/Negativity Score)

        self.plot(toPlot, keyword)
        return toPlot

    def fetchPopular(self, keyword, num, language='en'):
        api = self.api

        tweets = tweepy.Cursor(api.search, q=keyword,
                               lang=language, tweet_mode='extended', result_type='popular').items(num)

        toPlot = {}
        for tweet in tweets:
            # Analyse tweet
            toPlot[tweet.created_at] = self.analyse(
                tweet.full_text)  # (Positivity/Negativity Score)

        self.plot(toPlot, keyword)
        return toPlot

    def plot(self, toPlot, keyword):

        x_axis = []
        y_axis = []

        for x in sorted(toPlot.keys()):
            x_axis.append(x)
            y_axis.append(toPlot[x])

        # Plotting the graph
        plt.plot(x_axis[::-1], y_axis[::-1])
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Positivity")

        plt.title(f'Positivity graph for {keyword}')
        plt.show()


class MaxListener(tweepy.StreamListener):

    def on_status(self, status):

        if not status.truncated:
            tweet_text = status.text
        else:
            tweet_text = status.extended_tweet['full_text']

        if not status.retweeted and 'RT @' not in tweet_text:
            score = self.analyse(tweet_text)
            toPlot[status.created_at] = score
            print("Tweet created at", status.created_at,
                  'with a score of', score)

    def on_error(self, error):
        print(error)
        return False

    def analyse(self, text):
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)

        return scores['compound']*10


class MaxStream():

    def __init__(self, api, listener, keyword):
        self.stream = tweepy.Stream(auth=api.auth, listener=listener)
        self.keyword = [keyword]

    def start(self):

        keywords = self.keyword

        print('Monitoring...', keywords)
        print('Starting Stream')

        global toPlot
        toPlot = {}
        while True:
            try:
                self.stream.filter(track=keywords)
            except ProtocolError as pe:
                print(pe)
                continue
            except ec.TimeoutError as te:
                print(te)
                continue
            except ec.HTTPError as he:
                print(he)
                continue

            except KeyboardInterrupt:
                self.plot(toPlot)
                break

    def plot(self, toPlot):
        """A function to plot the real time data

        Args:
            toPlot (dictionary): A dictionary of tweets, and their respective scores
        """

        x_axis = []
        y_axis = []

        for x in sorted(toPlot.keys()):
            x_axis.append(x)
            y_axis.append(toPlot[x])

        # Plotting the graph
        plt.plot(x_axis[::-1], y_axis[::-1])
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Positivity")

        plt.title(f'Positivity graph for {self.keyword[0]}')
        plt.show()


def startStream(keyword):
    """A function to start streaming of real time data

    Args:
        keyword (string): Keyword to be monitored by the bot
    """

    # Authentication keys and tokens
    API_KEY = os.environ.get('API_KEY')
    API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    # Starting the stream
    listener = MaxListener(api)
    stream = MaxStream(api, listener, keyword)
    stream.start()


while True:

    # User input
    inp = input("""Enter your choice.
1. Get analysis for historical data
2. Get analysis for popular tweets
3. Start analysis of real time data
4. Quit
""")

    # Twitter object
    twitter = Twitter()

    if inp.lower() == 'historical':
        keyHist = input("""What keyword would you like to monitor?
""")
        dateHist = input("""What date would you like the data to be collected from? Format = "YYYY-MM-DD"
""")

        twitter.historical(keyHist, dateHist)

    elif inp.lower() == 'popular':
        keyPopular = input("""What keyword would you like to monitor?
""")
        numPopular = int(input("""What amount of popular tweets would you like to analyse?
"""))

        twitter.fetchPopular(keyPopular, numPopular)

    elif inp.lower() == 'real time':
        streamKey = input("""What keyword would you like to monitor?
""")

        startStream(streamKey)

    elif inp.lower() == 'quit':
        break

    else:
        print('Enter a valid response')
