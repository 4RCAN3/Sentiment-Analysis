# import required librareis
from matplotlib.pyplot import plot


try:
    import tweepy
    import datetime
    from dotenv import load_dotenv
    import os
    from nrclex import NRCLex
    import matplotlib
    from nltk.sentiment import SentimentIntensityAnalyzer
    import matplotlib.pyplot as plt
    import sys
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

        self.plot(toPlot)
        return toPlot

    def fetchTop(self, keyword, num, language='en'):
        api = self.api

        tweets = tweepy.Cursor(api.search, q=keyword,
                               lang=language, tweet_mode='extended').items(num)

        toPlot = {}
        for tweet in tweets:
            # Analyse tweet
            toPlot[tweet.created_at] = self.analyse(
                tweet.full_text)  # (Positivity/Negativity Score)

        self.plot(toPlot)
        return toPlot

    def plot(self, toPlot):

        x_axis = []
        y_axis = []
        for x in toPlot.keys():
            x_axis.append(x)
            y_axis.append(toPlot[x])

        # Plotting the graph
        plt.plot(x_axis[::-1], y_axis[::-1])
        plt.gcf().autofmt_xdate()
        plt.xlabel("Time")
        plt.ylabel("Positivity")

        plt.title('Positivity graph')
        plt.show()


twitter = Twitter()
twitter.historical('Minima Global', '2021-10-01')
twitter.fetchTop('Minima Global', 20)
