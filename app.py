import os
import logging
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from onboarding_tutorial import OnboardingTutorial
from PIL import Image
from requests_oauthlib import OAuth1Session
import urllib.request
import config
import json
import requests
from twitter import Twitter, OAuth

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# For simplicity we'll store our app data in-memory with the following data structure.
# onboarding_tutorials_sent = {"channel": {"user_id": OnboardingTutorial}}
onboarding_tutorials_sent = {}

ts_list = []

@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    event = payload.get("event", {})

    channel_id = event.get("item", {}).get("channel")
    user_id = event.get("user")
    reaction = event.get("reaction")
    item = event.get("item")
    ts = item.get("ts")

    user_info = slack_web_client.users_info(**{'user':user_id})
    user = user_info.get("user")
    user_name = user.get("real_name")


    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(payload)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    print(user_name)

    if "青木允輝"in user_name and reaction == 'white_check_mark' and ts not in ts_list :
        response = slack_web_client.reactions_get(**{'channel':channel_id , 'timestamp': ts})
        message = response.get("message")
        text = message.get("text")
        files = message.get("files")
        if files != None:
            file_check = True
        else:
            file_check = False
        urls = []

        print("\n\n\n\n\n\n\n\n")
        print(file_check)
        print("\n\n\n\n\n\n\n\n")

        if file_check == True:
            for photo in files:
                photo_id = photo.get('id')
                print(photo_id)
                try:
                    slack_web_client.files_sharedPublicURL(token=os.environ['ACCESS_TOKEN'],file = photo_id)
                except:
                    pass
                url_private = photo.get('url_private')
                url = photo.get('permalink_public')
                permanents = url.split('-')
                permanent = permanents[-1]
                url = url_private + '?pub_secret=' + permanent
                urls.append(url)

            i = 0
            for url in urls:
                dst_path = 'py-logo'+ str(i) + '.png'
                download_file(url, dst_path)
                i = i + 1 
        

        ts_list.append(ts)
        
        print(response)

        try:
            if file_check == True: 
                tweet_img(urls,text)
            else:
                tweet(text)
            text='正常にツイートしました'
            slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")
            print(response)
        except:
            text='ツイートに失敗しました'
            slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")

    if "青木允輝"in user_name and reaction == 'white_check_mark' and False and ts not in ts_list :
        response = slack_web_client.reactions_get(**{'channel':channel_id , 'timestamp': ts})
        message = response.get("message")
        text = message.get("text")
        files = message.get("files")
        if files != None:
            file_check = True
        else:
            file_check = False
        urls = []

        print("\n\n\n\n\n\n\n\n")
        print(files)
        print("\n\n\n\n\n\n\n\n")

        if file_check == True:
            for photo in files:
                photo_id = photo.get('id')
                print(photo_id)
                try:
                    slack_web_client.files_sharedPublicURL(token=os.environ['ACCESS_TOKEN'],file = photo_id)
                except:
                    pass
                url_private = photo.get('url_private')
                url = photo.get('permalink_public')
                permanents = url.split('-')
                permanent = permanents[-1]
                url = url_private + '?pub_secret=' + permanent
                urls.append(url)

                text = url

            i = 0
            for url in urls:
                dst_path = 'py-logo'+ str(i) + '.png'
                download_file(url, dst_path)
                i = i + 1
        
            ts_list.append(ts)
            
            try:
                if file_check == True: 
                    tweet_img(urls,text)
                    print("ぺろ")
                else:
                    tweet(text)
                text='正常にツイートしました'
                slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=url,thread_ts=ts,username="TWEET_SUBMIT")
                print(response)
            except:
                text='ツイートに失敗しました'
                slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")
                print(urls)
        else:
            text='投稿には画像が必要です。'
            slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")





def tweet(text):    

    CK=os.environ['TW_CONSUMER_KEY']
    CS=os.environ['TW_CONSUMER_SECRET']
    AT=os.environ['TW_TOKEN']
    AS=os.environ['TW_TOKEN_SECRET']

    twitter = OAuth1Session(CK,CS,AT,AS)

    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    status = text

    params = {"status": status}

    twitter.post(url_text,params=params)



def tweet_img(img_url,text):    

    CK=os.environ['TW_CONSUMER_KEY']
    CS=os.environ['TW_CONSUMER_SECRET']
    AT=os.environ['TW_TOKEN']
    AS=os.environ['TW_TOKEN_SECRET']

    twitter = OAuth1Session(CK,CS,AT,AS)

    url_media = "https://upload.twitter.com/1.1/media/upload.json"

    url_text = "https://api.twitter.com/1.1/statuses/update.json"

    media_id = []

    for i in range(len(img_url)):

        headers = {"User-Agent": "Mozilla/5.0"}

        request = urllib.request.Request(url=img_url[i],headers=headers)

        response = urllib.request.urlopen(request)

        data = response.read()

        files = {"media" : data}

        req_media = twitter.post(url_media,files = files)

        media_id.append(json.loads(req_media.text)['media_id_string'])

    media_id= ','.join(media_id) 

    status = text

    params = {"status": status, "media_ids": media_id}

    twitter.post(url_text,params=params)


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)