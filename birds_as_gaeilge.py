#!/usr/bin/env python

import json
import requests
import urllib.request

import numpy as np
import pandas as pd
import wikipedia

from pathlib import Path

from mastodon import Mastodon

def get_wiki_image(search_term):
    """
    Search wikipedia for thumbnail image
    https://stackoverflow.com/a/61103584
    """
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0


mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://mastodon.ie/'
)

image_path = Path("./images/birds")
dict_file = Path("EnglishLatinIrish.htm")
df = pd.read_html(dict_file)[0]
# remove fluff
df = df.drop(index=[0,1,2,426, 427], columns = [3,4,5])
df = df.reset_index(drop=True)

rng = np.random.default_rng()
r_ind = rng.integers(0, len(df))
random_bird = df.loc[r_ind]
english_name = random_bird[0]
latin_name = random_bird[1]
irish_name = random_bird[2]

# WIKI_REQUEST = "http://en.wikipedia.org/w/api.php?action=query&titles="
WIKI_REQUEST ='http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
bird_image_url = get_wiki_image(latin_name)
bird_image_file_name = image_path/(latin_name.replace(' ', '_')+Path(bird_image_url).suffix)
urllib.request.urlretrieve(bird_image_url, bird_image_file_name)

bird_page = wikipedia.page(latin_name)

media = mastodon.media_post(bird_image_file_name, description="An image of {}, presumably.".format(english_name))
mastodon.status_post("The {} ({}, {}) is known as {} as Gaeilge.".format(
    english_name,
    latin_name,
    bird_page.url,
    irish_name
    ),
    media_ids=media
)