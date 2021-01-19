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


def start_onboarding(user_id: str, channel: str):
    # Create a new onboarding tutorial.
    onboarding_tutorial = OnboardingTutorial(channel)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
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

    print(user_name)

    if "青木允輝"in user_name and "AoKoM" in user_name and reaction == 'white_check_mark' and ts not in ts_list :
        response = slack_web_client.reactions_get(**{'channel':channel_id , 'timestamp': ts})
        message = response.get("message")
        text = message.get("text")
        files = message.get("files")
        file_check = False
        urls = []

        if len(files) > 0 :
            file_check = True
        
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

        print(urls)

        ts_list.append(ts)

        t = Twitter(
            auth=OAuth(
                config.TW_TOKEN,
                config.TW_TOKEN_SECRET,
                config.TW_CONSUMER_KEY,
                config.TW_CONSUMER_SECRET,
            )
        )

        print(urls)

        i = 0
        for url in urls:
            dst_path = 'py-logo'+ str(i) + '.png'
            download_file(url, dst_path)
            i = i + 1 

        reply = text
        print(reply)

        slack_web_client.chat_postMessage(token=os.environ['ACCESS_TOKEN'],channel=channel_id,text=text,thread_ts=ts,username="TWEET_SUBMIT")

        url = Image.open('sample.png')

        call(urls)

        print(text)
        print(type(url))

@slack_events_adapter.on("message")
def message(payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    print(payload)    


def call(img_url):    

    CK=config.TW_CONSUMER_KEY

    CS=config.TW_CONSUMER_SECRET

    AT=config.TW_TOKEN

    AS=config.TW_TOKEN_SECRET

    twitter = OAuth1Session(CK,CS,AT,AS)

    url_media = "https://upload.twitter.com/1.1/media/upload.json"

    url_text = "https://api.twitter.com/1.1/statuses/update.json"

#    img_url = ['https://files.slack.com/files-pri/T01G53S0SSD-F01JS3CRH6D/mojomoji.png?pub_secret=7fb12ecb60',

#           'https://1.bp.blogspot.com/-CSIokkL0VJc/XVKgHNKp2QI/AAAAAAABUHU/znkuxlOlQ5giZ3gDbks7KAK3TJnT2q1XwCLcBGAs/s1600/kotowaza_hato_mamedeppou.png',

#            'https://1.bp.blogspot.com/-8sMAiPmvFuo/XVjgKN2BXoI/AAAAAAABUM0/IfTQp8hHWRsVk_u7s84OE6yvFJ5ekpnLwCLcBGAs/s1600/kid_seikaku_uchiki_girl.png',

#           'https://1.bp.blogspot.com/-ahlT7Kd7-T0/XVjgJ3hrbFI/AAAAAAABUMw/MV4su85SnoAMYnSitR9DXVgNFuorpprwQCLcBGAs/s1600/kid_seikaku_uchiki_boy.png']  #①

    media_id = []

    for i in range(len(img_url)):

        headers = {"User-Agent": "Mozilla/5.0"}  #②

        request = urllib.request.Request(url=img_url[i],headers=headers)

        response = urllib.request.urlopen(request)

        data = response.read()

        files = {"media" : data}

        req_media = twitter.post(url_media,files = files)  #③

        media_id.append(json.loads(req_media.text)['media_id_string'])

    media_id= ','.join(media_id)  #④

    status = "test"

    params = {"status": status, "media_ids": media_id}

    stri = "アイウエオ"

    print(stri+"ペロペロ")

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

