from datetime import date, timedelta
from getPatents import patent_list
from account import *
import tweepy


def login():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api


def get_tweets():
    date2 = date.today() - timedelta(7305)
    date1 = date2 - timedelta(14)

    return patent_list(date1, date2)

bot = login()
tweet = get_tweets()

bot.update_status(tweet)