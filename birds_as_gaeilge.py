#!/usr/bin/env python

import numpy as np
import pandas as pd

from pathlib import Path

from mastodon import Mastodon

mastodon = Mastodon(
    access_token = 'token.secret',
    api_base_url = 'https://mastodon.ie/'
)

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

mastodon.status_post("The {} ({}) is known as {} as Gaeilge.".format(
    english_name,
    latin_name,
    irish_name
))