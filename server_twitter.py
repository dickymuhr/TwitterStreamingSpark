import tweepy
import socket

ACCESS_TOKEN = "1587245730-fAptYxzE2j5dmeDVOsTgnc9n5x04ixoqBaDHIL5"
ACCESS_SECRET = "1RyzyrK3FtWsMQ2PI16l7Fr3aXbSq2TCuSiPOEDqSIMPc"
CONSUMER_KEY = "E14cvoVsBtHBDXf3UVaPbp5c4"
CONSUMER_SECRET = "d9wE84a9S9ME7rLGva0lxPDjGxsZHBMx2dfT7kwmlY0mNRgp1C"

# authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

class Listener(tweepy.Stream):
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET ,csocket):
        super().__init__(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        self.client_socket = csocket
    count = 0
    tweets = []
    limit = 100000
    def on_status(self, status):

        try:
            msg = ""
            if not status.truncated:
                msg = status.text
            else:
                msg = status.extended_tweet['full_text']
            msg = msg + " "
            self.tweets.append(msg)
            print(msg.encode('utf-8'))
            self.client_socket.send(msg.encode('utf-8'))
            self.count += 1
            print(f"============== Tweet ke: {self.count} ==============")
            if len(self.tweets) == self.limit:
                self.disconnect()
                return True
        except BaseException as e:
            print("Error on_data: %s" %str(e))
        return True
    def on_error(self, status):
        print(status)
        return True

def sendData(c_socket):
    stream_tweet = Listener(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, c_socket)
    stream_tweet.filter(track=['kanjuruhan'])

s = socket.socket()
host = "127.0.0.1"
port = 9091
s.bind((host,port))
print("Listening on port: %s"%str(port))

s.listen(5)
c, addr = s.accept()
print("Received request from: " + str(addr))

sendData(c)