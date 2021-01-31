import requests
import urllib
import json
import os
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter



app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)
photo_id = 'F01KHN24751'

slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

slack_web_client.files_sharedPublicURL(token=os.environ['ACCESS_TOKEN'],file = photo_id)



def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

response = requests.get('https://slack-files.com/T01G53S0SSD-F01KHN24751-f8bf3077d8')


with open('sample.mp4', 'wb') as saveFile:
    saveFile.write(response.content)

download_file('https://slack-files.com/T01G53S0SSD-F01KHN24751-f8bf3077d8', 'sample2.mp4')