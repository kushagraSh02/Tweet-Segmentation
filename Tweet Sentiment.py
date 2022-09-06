import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    def __init__(self):
        consumer__key = 'NhqKuP46Dx82ji8WQvo0HuDXd'
        consumer__secret = 'Cc0RwOhgnrYwUSI1PHTVvkStI4ntCDldAiv1dO1QQmE4oToaiy'
        access_token = "1146523362522361856-fNoF1efBHkqZfjp8v9Ve0u0spSZyLi"
        access_secret = 'lfxNnEjTE2z67S5elIZToszvuo5gWZ40q5OF30nnNvG5F'

        try:
            self.auth = OAuthHandler(consumer__key, consumer__secret)
            self.auth.set_access_token(access_token, access_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed!")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ', tweet).split())

    def get_tweet_sentiment(self, tweet):
            analysis = TextBlob(self.clean_tweet(tweet))

            if analysis.sentiment.polarity > 0:
                return 'positive'
            elif analysis.sentiment.polarity == 0:
                return 'neutral'
            else:
                return 'negative'

    def get_tweet(self, query, label='TweetKushagra'):
        tweets=[]
        try:
            fetched_tweets = self.api.search_30_day(label=label, query=query)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepyException as e:
            print("Error: "+str(e))


def main():
    api = TwitterClient()
    tweets = api.get_tweet(query = "Narendra Modi")
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    print("Neutral tweets percentage: {} % \
           ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()