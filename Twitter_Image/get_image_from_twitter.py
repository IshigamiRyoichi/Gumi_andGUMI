import os
import tweepy
import time
import urllib.request, urllib.error
import json

open_json = open("../assets/login.json")
api_json = json.load(open_json)

save_folder = "./gumi_folder/"
os.makedirs(save_folder, exist_ok=True)

API_KEY = api_json["API_Key"]
API_SECRET_KEY = api_json["API_secret_key"]
ACCESSS_TOKEN = api_json["API_access_token"]
ACCESSS_SECRET_TOKEN = api_json["API_access_scret_token"]

find_key = ["#Gumi","#グミ"]


page_num = 25
tweet_num = 25

class image_Downloads(object):
    def __init__(self):
        super(image_Downloads, self).__init__()
        self.set_api()

    def run(self):
        self.max_id = None
        for _ in range(page_num):
            for target in find_key:
                ret_url_list = self.search(target, tweet_num)
                print(ret_url_list)
                for url in ret_url_list:
                    self.download(url)
            time.sleep(0.1)

    def set_api(self):
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESSS_TOKEN, ACCESSS_SECRET_TOKEN)
        self.api = tweepy.API(auth)

    def search(self, target, rpp):
        ret_url_list = []
        try:
            if self.max_id:
                res_search = self.api.search_tweets(q=target, lang='ja', rpp=rpp, max_id=self.max_id)
            else:
                res_search = self.api.search_tweets(q=target, lang='ja', rpp=rpp)
            for result in res_search:
                if "media" not in result.entities:
                    continue
                for media in result.entities['media']:
                    url = media['media_url_https']
                    if url not in ret_url_list:
                        ret_url_list.append(url)
            self.max_id = result.id
            return ret_url_list
        except Exception as e:
            self.error_catch(e)
    
    def download(self, url):
        url_orig = "%s:orig" % url
        path = save_folder + url.split("/")[-1]
        try:
            response = urllib.request.urlopen(url=url_orig)
            with open(path,"wb") as f:
                f.write(response.read())
        except Exception as e:
            self.error_catch(e)

    def error_catch(self, error):
        print("error:",error)

def main():
    try:
        downloader = image_Downloads()
        downloader.run()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()