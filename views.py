from flask import Blueprint, render_template
import random, psycopg2
#from tweet_data import tweet_dictionary, other_tweet_dictionary

views = Blueprint(__name__, "views")

conn = psycopg2.connect(
                    host = "localhost",
                    database = "twotter_db",
                    user = "user",
                    password = "password")
tweet_cursor = conn.cursor()

def get_tweet():
    tweet_cursor.execute("SELECT MAX(tweetid) from tweets""")
    MAX_SIZE = tweet_cursor.fetchall()[0][0]
    random_number = random.randint(0, MAX_SIZE)
    get_tweet = f""" SELECT * FROM tweets where TweetID = {random_number}"""
    tweet_cursor.execute(get_tweet)
    _, userid, date, content = tweet_cursor.fetchall()[0]
    get_user = f""" SELECT * FROM users where UserID = {userid}"""
    tweet_cursor.execute(get_user)
    _, name, handle, following, followers = tweet_cursor.fetchall()[0]
    tweet_cursor.execute(get_tweet)
    tweet = {"user": name,
            "username": handle,
            "date": date,
            "content" : content }
    return tweet

def populate_tweets(number):
    tweet_dictionary = {}
    for i in range(number):
        tweet_dictionary["tweet" + str(i)] = get_tweet()
    return tweet_dictionary


@views.route("/")
def home():
    return render_template("index.html",
                    tweet_dictionary=populate_tweets(10),
                    other_tweet_dictionary=populate_tweets(10))

@views.route("/home")
def home2():
    return "Hello World:  This is my homepage."


populate_tweets(5)
