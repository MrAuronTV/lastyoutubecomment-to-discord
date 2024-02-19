#!/usr/bin/env python3
import os
import pickle
import requests
import json
import time
from urllib import request
from urllib.error import HTTPError
from json import loads

PATH = '/PATH/TO/SCRIPT' #Path where you stock stream id for doesnt spam discord
WEBHOOK = "WEBHOOK_URL" #webhook url discord
CHANNEL_ID = 'CHANNEL_ID'
API_KEY = 'YOUR_API_KEY'

try:
    id = pickle.load(open("{}/lastcomment".format(PATH), "rb"))

except (OSError, IOError) as e:
    foo = 3
    pickle.dump(foo, open("{}/lastcomment".format(PATH), "wb"))

API_ENDPOINT = 'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&allThreadsRelatedToChannelId={0}&moderationStatus=published&order=time&textFormat=plainText&key={1}&maxResults=1'.format(CHANNEL_ID,API_KEY)
r = requests.get(url = API_ENDPOINT)

COMMENT = loads(r.text)['items'][0]['snippet']['topLevelComment']['snippet']['textDisplay'] #GET COMMENT
COMMENTID = loads(r.text)['items'][0]['snippet']['topLevelComment']['id'] #GET COMMENT ID
AUTHOR = loads(r.text)['items'][0]['snippet']['topLevelComment']['snippet']['authorDisplayName'] #GET COMMENT AUTHOR
PUBLISH = loads(r.text)['items'][0]['snippet']['topLevelComment']['snippet']['publishedAt'] #GET DATE
VIDEOID = loads(r.text)['items'][0]['snippet']['videoId'] #GET VIDEOID

# La payload
payload = {
    'username':"USERNAME",
    'content': "MESSAGE CONTENT",
    'avatar_url':"AVATAR URL",
    'embeds': [
        {
            'title': COMMENT,  # Le titre de la carte
            'url': 'https://www.youtube.com/watch?v={0}&lc={1}&feature=em-comments'.format(VIDEOID,COMMENTID),
            "color": 16711680,
            'author': {'name': AUTHOR},  # Pourquoi pas mettre des auteurs ?
            'timestamp': PUBLISH,
        },
    ]
}

# Les paramètres d'en-tête de la requête
headers = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
}

req = request.Request(url=WEBHOOK,
                      data=json.dumps(payload).encode('utf-8'),
                      headers=headers,
                      method='POST')

if COMMENTID:
    if COMMENTID != id :
       response = request.urlopen(req)
with open('{}/lastcomment'.format(PATH), 'wb') as f:
    pickle.dump(COMMENTID, f)
