from instagram_private_api import Client, ClientCompatPatch
from PIL import Image
import io
import urllib.request
import os

user_name = 'go_kawamitsu'
password = os.environ['INSTA_PASSWORD']
api = Client(user_name, password)

# 画像のURL
url = "https://user-images.githubusercontent.com/5179467/57978324-23e4b000-7a46-11e9-8b04-4d16e97a702c.jpg"

# 画像データを取得する
img_in = urllib.request.urlopen(url).read()
img_bin = io.BytesIO(img_in)
img = Image.open(img_bin)

# 画像を投稿する
api.post_photo(img_bin.getvalue(), (img.width, img.height))