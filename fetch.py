import tweepy
import json
# Consumer key i secret generisemo na twitter stranici (Aplikacija)
consumer_key = 'Hit30sfZfVKpgFBTvLdtOJvRd'  # Api Key
consumer_secret = 'CWXkO2b9paBGcQaXhPdHXJYqViM8gjrUFKxAK1bRcyUegCRMT8'  # Api Secret

# Bearer token za API v2 auth
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPXGZwEAAAAAGCCa45eFyu0OY22a1J3pF3NhjtA%3DjRP5DaDcRNjy5RhByB8ganco9PMgpIBDoMTcgL1jCdQmg2g2KF'

# Api token i secret za pristup naloga
access_token = '2504267706-6Rw1fjZ7h3AtnyJ7ou3NoznipELm2U5v5MJLnN5'
access_token_secret = 'EjifJCswpL8XhBxvxwKV4YERZcGJv49mFOWg0LGtA2rpd'

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

# Kreiramo api objekat i postavljamo wait_on_limit na True kako bi u slučaju do dostignemo rate limit kod sačekao,
# pre sledećeg korišćenja apija
api = tweepy.API(auth, wait_on_rate_limit=True)

screen_name = 'Blic_online'
tweets = api.user_timeline(screen_name=screen_name,
                           # 200 je max
                           count=200,
                           # Ne želimo retweetove
                           include_rts=False,
                           # Potrebno kako bi dobili ceo tekst, u protivnom dobicemo samo prvih 140 karaktera
                           tweet_mode='extended'
                           )

all_tweets = []
all_tweets.extend(tweets)
oldest_id = tweets[-1].id
while True:
    tweets = api.user_timeline(screen_name=screen_name,
                               # 200 is the maximum allowed count
                               count=200,
                               include_rts=False,
                               max_id=oldest_id - 1,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode='extended'
                               )
    # Ako je broj dobavljenih tweetova 0 izlazimo iz petlje
    if len(tweets) == 0:
        break
    # Postavljamo oldest_id na poslednji dobijeni tweet
    oldest_id = tweets[-1].id
    # Nove tweetove dodajemo u listu svih tweetova
    all_tweets.extend(tweets)
    print('Preuzeto tweetova: ', len(all_tweets))

with open('out/fetch_data.json', 'w', encoding='utf-8') as f:
    for tweet in all_tweets:
        print(tweet._json)
        f.write(json.dumps(tweet._json, indent=4) + '\n')
