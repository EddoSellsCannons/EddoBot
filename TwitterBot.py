import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("Cdt1y4lZUpFzpN0EJpFwUsmwH", "Ft29tROmZQnkf9Cx7cvQULSlSsJSNb167V8afOJj9JpRwpeXHY")
auth.set_access_token("810369363962396672-36th1wyw6dBJZoUHKFOKmGeGxUxX3pp", "sYQ3w0eAh4t61DPzUlPyFL8HaZuyD3FeYqWx94LIrI3cU")

# Create API object
api = tweepy.API(auth)

timeline = api.home_timeline()
#for tweet in timeline:
#    print(f"{tweet.user.name} said {tweet.text}")

# Create a tweet
def send_tweet(msg):
    try:
        api.verify_credentials()
        api.update_status(msg)
    except:
        print("Error Authenticating.")
        raise IndexError

#count characters in text
def count_characters(txt):
    total = 0
    for c in txt:
        total += 1
    return total

#update bio of eddobot
def update_bio(bio):
    try:
        api.verify_credentials()
        if count_characters(bio) < 160:
            api.update_profile(description=bio)
    except:
        print("Error Authenticating.")
        raise IndexError

