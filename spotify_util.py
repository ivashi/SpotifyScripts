import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_ID = os.getenv('SECRET_ID')
SCOPE = 'playlist-modify-public'
REDIRECT_URI = "http://localhost:8888/callback"


def do_spotify_auth(username):
	token = util.prompt_for_user_token(username, SCOPE, client_id=CLIENT_ID,client_secret=SECRET_ID,redirect_uri=REDIRECT_URI)
	if token: 
		return spotipy.Spotify(auth=token)
	else: 
		sys.exit(f"Can't get token for {username}")