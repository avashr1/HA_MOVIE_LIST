#!/usr/bin/env python
import os
import requests
import re
import time

from dotenv import load_dotenv

import insert_into_db

# Load secrets from a local .env file (see .env.example). Never commit real tokens.
load_dotenv()

w_delete = False
access_token = os.environ.get('PUSHBULLET_ACCESS_TOKEN')
tmdb_token = os.environ.get('TMDB_API_TOKEN')

if not access_token or not tmdb_token:
    raise SystemExit("Missing PUSHBULLET_ACCESS_TOKEN or TMDB_API_TOKEN. Copy .env.example to .env and fill in your values.")

headers = {
    'Access-Token': access_token
}

# Initial payload
# Note: 'limit' defaults to around 20 if not specified.
# We set it to 500 (max) to reduce the number of requests.
payload = {
    'active': 'true',
    'modified_after': '1.4e+09',
    'limit': '500'
}

url = 'https://api.pushbullet.com/v2/pushes'

print("Starting extraction...")

while True:
    # Make the GET request

    response = requests.get(url, headers=headers, params=payload)

    if response.status_code != 200:
        print("Failed to retrieve data, status code:", response.status_code)
        break

    data = response.json()

    # Process the current batch of pushes
    if 'pushes' in data:
        for item in data['pushes']:
            # Check if the push is a link and has a url
            if item.get('type') == 'link' and 'url' in item:
                push_url = item['url']

                # Combined Regex to catch both mobile (m.) and www. imdb links
                # This looks for 'http' + optional 's' + '://' + optional 'm.' or 'www.' + 'imdb.com/title/'
                match = re.search(r'imdb\.com/title/(tt\d+)', push_url)

                if match:
                    imdb_id = match.group(1)

                    url_themd = f"https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id&language=en-US"
                    headers_themd = {
                        "accept": "application/json",
                        "Authorization": f"Bearer {tmdb_token}"
                    }

                    response_themd = requests.get(url_themd, headers=headers_themd)
                    data_themd = response_themd.json()
                    if data_themd.get('movie_results'):
                       for movie in data_themd.get('movie_results'):
                        insert_into_db.save_movie_to_db(imdb_id, movie.get('title'),movie.get('poster_path'))

                        #print(f"Found ID: {imdb_id} (from {push_url})")

    # --- PAGINATION LOGIC ---
    # Check if the response contains a 'cursor', indicating more pages exist
    if 'cursor' in data:
        payload['cursor'] = data['cursor']
        #print(f"--- Moving to next page (Cursor: {data['cursor'][:10]}...) ---")
        time.sleep(0.1)  # Be polite to the API
    else:
        #print("No more cursor found. Extraction complete.")
        w_delete = True
        break

if w_delete:

  headers = {'Access-Token': access_token}

  url = 'https://api.pushbullet.com/v2/pushes'

  response = requests.delete(url, headers=headers)