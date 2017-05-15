import tweepy
import time
import sys
import csv
from textblob import TextBlob

def tweet_sentiment(username):

    try:
        auth = tweepy.OAuthHandler(ck, cs)
        auth.set_access_token(at, ats)
        api = tweepy.API(auth)
        tweets_for_csv = []
        number_of_tweets = 100    #fetching only 100 tweets of user
        tweets = api.user_timeline(screen_name = username,count = number_of_tweets)
        for tweet in tweets:
            blob = TextBlob(tweet.text.encode("ascii","ignore"))
            if blob.sentiment.polarity > 0:
                temp = [tweet.text.encode("ascii","ignore"), blob.sentiment.polarity, "positive"]
                tweets_for_csv.append(temp)
            elif blob.sentiment.polarity < 0:
                temp = [tweet.text.encode("ascii","ignore"), blob.sentiment.polarity, "negative"]
                tweets_for_csv.append(temp)
            if blob.sentiment.polarity > 0:
                temp = [tweet.text.encode("ascii","ignore"), blob.sentiment.polarity, "neutral"]
                tweets_for_csv.append(temp)
        
        print "writing to {0}_tweets.csv".format(username)
        with open("{0}_tweets.csv".format(username) , 'w+') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(tweets_for_csv)
            
    except tweepy.TweepError:
        print "Failed to extract tweets of",username

ck = ""						#copy paste your consumer key
cs = ""						#copy paste your consumer secret
at = ""						#copy paste your access token
ats = ""					#copy paste your access token secret

auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(at, ats)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

ids = []
for page in tweepy.Cursor(api.followers, screen_name="").items():	#key in the desired username
	print page.screen_name
	ids.append(page.screen_name)
	time.sleep(10)

for user in ids:
    user = "@"+user.encode('ascii','ignore')
    tweet_sentiment(user)
