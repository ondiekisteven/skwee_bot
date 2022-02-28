import aiohttp
import json

import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import base64
from lyricsgenius import Genius as GeniusLyrics


class Genius:
    def __init__(self, aiohttp_session: ClientSession = None):
        self.token = 'ixSPr24nAw6FnPZVDGWpWPl40zirdftUk6x7gO5llceXb2v-Ey2Q7SBQaJ9QKksm'
        self.APIUrl = 'https://api.genius.com/'
        self.session = aiohttp_session

    def lyrics(self, song_id):
        return GeniusLyrics(self.token).lyrics(song_id)

    def get_header(self):
        header = {
            'Authorization': f'Bearer {self.token}',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
        return header

    def make_query_from_params(self, params):
        query_string = f'?access_token={self.token}'
        for key in params.keys():
            value = params[key]
            query_string += f"&{key}={value}"
        return query_string

    def make_request(self, method, params=None, path=None):
        headers = {'Authorization': f'Bearer {self.token}'}
        if params and path:
            result = requests.get(f'{self.APIUrl}{method}/{path}', params=params, headers=headers)
            return result.text
        elif params:
            result = requests.get(self.APIUrl + method, params=params, headers=headers)
            return result.text

    def get_json(self, path, params=None, headers=None):
        """Send request and get response in json format."""

        # Generate request URL
        requrl = ''.join([self.APIUrl, path])
        token = "Bearer {}".format(self.token)
        if headers:
            headers['Authorization'] = token
        else:
            headers = {"Authorization": token}

        # Get response object from querying genius api
        response = requests.get(url=requrl, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def connect_lyrics(self, song_id):
        """Constructs the path of song lyrics."""
        url = "songs/{}".format(song_id)
        data = self.get_json(url)

        # Gets the path of song lyrics
        path = data['response']['song']['path']

        return path

    def search_song(self, search_term):
        params = {'q': search_term}
        result = self.make_request('search', params=params)
        result = json.loads(result)
        if result['meta']['status'] == 200:
            try:
                pass
            except IndexError:
                return "Could not find song"
            song = result['response']['hits'][0]['result']
            song_id = song['id']
            song_title = song['full_title']
            song_thumbnail = song['header_image_thumbnail_url']
            return {
                'song_id': song_id,
                'song_title': song_title,
                'song_thumbnail': song_thumbnail
            }
        else:
            return 'Could not find song'

    def retrieve_lyrics(self, song_id):
        '''Retrieves lyrics from html page.'''
        try:
            path = self.connect_lyrics(song_id)
            URL = "http://genius.com" + path
            page = requests.get(URL)
            # Extract the page's HTML as a string
            html = BeautifulSoup(page.text, "lxml")

            # Scrape the song lyrics from the HTML
            lyr = html.find("div", class_="lyrics").get_text()
        except AttributeError:
            lyr = 'Could not find lyrics. Try again with different keywords'
        return lyr

    def encode_audio(self, file_path):
        f = open(file_path, 'rb')
        contents = f.read()
        return base64.encodebytes(contents)
