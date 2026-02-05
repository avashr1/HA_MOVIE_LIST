#!/usr/bin/env python
import requests
import re
import time

import insert_into_db

w_delete = False
# Replace '<your_access_token_here>' with your actual access token
access_token = 'REDACTED_PUSHBULLET_TOKEN'

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
                        "Authorization": "Bearer REDACTED_TMDB_TOKEN"
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

  headers = {'Access-Token': 'REDACTED_PUSHBULLET_TOKEN'}

  url = 'https://api.pushbullet.com/v2/pushes'

  response = requests.delete(url, headers=headers)