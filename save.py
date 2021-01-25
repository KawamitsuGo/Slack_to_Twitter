import requests
import urllib
import json

def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

response = requests.get('https://files.slack.com/files-pri/T01G53S0SSD-F01KHN24751/v070256b0000bobdocvhplilobjpasd0.mp4?pub_secret=f8bf3077d8')

response.dumps()

with open('sample.mp4', 'wb') as saveFile:
    saveFile.write(response.content)

download_file('https://files.slack.com/files-pri/T01G53S0SSD-F01KHN24751/v070256b0000bobdocvhplilobjpasd0.mp4?pub_secret=f8bf3077d8', 'sample2.mp4')