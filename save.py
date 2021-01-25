import requests
response = requests.get('https://files.slack.com/files-pri/T01G53S0SSD-F01KHN24751/download/v070256b0000bobdocvhplilobjpasd0.mp4')
with open('sample.mp4', 'wb') as saveFile:
    saveFile.write(response.content)