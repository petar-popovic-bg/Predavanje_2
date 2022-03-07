import tweepy
import json

# Consumer key i secret geisemo na twitter stranici (Aplikacija)
consumer_key = 'Hit30sfZfVKpgFBTvLdtOJvRd'  # Api Key
consumer_secret = 'CWXkO2b9paBGcQaXhPdHXJYqViM8gjrUFKxAK1bRcyUegCRMT8'  # Api Secret

# Bearer token za API v2 auth
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAPXGZwEAAAAAGCCa45eFyu0OY22a1J3pF3NhjtA%3DjRP5DaDcRNjy5RhByB8ganco9PMgpIBDoMTcgL1jCdQmg2g2KF'

# Api token i secret za pristup naloga
access_token = '2504267706-6Rw1fjZ7h3AtnyJ7ou3NoznipELm2U5v5MJLnN5'
access_token_secret = 'EjifJCswpL8XhBxvxwKV4YERZcGJv49mFOWg0LGtA2rpd'

# Kreiramo auth objekat i prosleđujemo mu neophodne parametre
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

# Kreiramo api objekat pomoću kojeg šaljemo upite
api = tweepy.API(auth)

# Ako je authentikacija uspela ispisujemo korisničko ime i id
print(api.verify_credentials().screen_name)
print(api.verify_credentials().id)

# Lista naloga koje želimo da pratimo
accounts = ['ALOnovine', 'PolitikaJavlja', 'Blic_online', 'pettar92']
follow_list = []

# Popunnjavamo listu id naloga koje zelimo da pratimo na streamu
for account in accounts:
    # Saljemo upit preko api objekta i zahtevamo tweepy User objekat na osnovu screen_name parametra
    user = api.get_user(screen_name=account)
    print(type(user), user.id)
    # Vadimo id iz dobijene instance modela
    uid = user.id
    # dodajemo dobijeni id u listu
    follow_list.append(uid)

# follow_list = [api.get_user(screen_name=account).id for account in accounts]


print(follow_list)


# Nasleđujemo tweepy.Stream klasu i modifikujemo je
class Stream(tweepy.Stream):
    # definišemo fajl
    out_file = open('out/stream_data.json', 'a', encoding='utf-8')

    # Override on?status metode, ispisujemo json
    def on_status(self, status):
        print(json.dumps(status._json))
        self.out_file.write(json.dumps(status._json, indent=4) + '\n')

    def on_connect(self):
        print('Stream connected!')

    def on_disconnect(self):
        print('Stream disconnected! / Closing out file.')
        self.out_file.close()


# Kreiramo stream objekat koji ćemo slušati, prosleđujemo parametre za autentifikaciju
stream = Stream(consumer_key, consumer_secret, access_token, access_token_secret)

# Pokrećemo stream
stream.filter(follow=follow_list)
