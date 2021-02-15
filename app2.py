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
        


        try:
            if file_check == True: 
                tweet_img(urls,text)
            else:
                tweet(text)
            text='正常にツイートしました'
            slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")
        except:
            text='ツイートに失敗しました'
            slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")

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

        print(response)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)

