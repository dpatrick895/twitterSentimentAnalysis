from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sqlite3
import twitterTokens as tt #this module is not necessary however I have done this to obscure my key and tokens

ckey = tt.getCkey()
csecret = tt.getCsecret()
atoken = tt.getAtoken()
asecret = tt.getAsecret()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS tweetsDB(username TEXT, tweet TEXT)")

class listener(StreamListener):
    
    def on_data(self, data):
        
        try: 
        
            all_data = json.loads(data)
            tweet = all_data["text"]
            username = all_data["user"]["screen_name"]
           
            localtime = time.asctime( time.localtime(time.time()) )
            print(tweet)
            print(username)
            dynamic_data_entry(username, tweet)
            
        
            return True
        except (BaseException, e):
            print("Failed ondata, ", str(e))
            
            c.close()
            conn.close()
            time.sleep(5)
    
    def on_error(self, status):
        print(status)

conn = sqlite3.connect('tweets.db')
c = conn.cursor()
create_table()

def dynamic_data_entry(username, tweet):
    
    c.execute("INSERT INTO tweetsDB (username, tweet) VALUES (?,?)", 
             (username, tweet))
    
    conn.commit()
    
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())

twitterStream.filter(track=["car"])
