from django.shortcuts import render
from tweepy import OAuth2BearerHandler, Client

def index(request):
    client = Client('AAAAAAAAAAAAAAAAAAAAAHaqoAEAAAAAGze%2BBaSNg1EkO2vTpkln6obIglU%3DGpFNZlQTPBVoZyNo5ENQueRlhl4EkCDpcgJYcQ31MFl3vkKfgK')

    QUERY = "#durhamcityharriers -filter:retweets"
    tweets = client.search_recent_tweets(query=QUERY)
    text ='<br>'
    for i in tweets:
        text += i.full_text + '</br>' 
