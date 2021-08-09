import argparse
import logging
import os
import pprint
import sys

# Spotify Specific
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_ID = os.getenv('SECRET_ID')
USERNAME = os.getenv('USERNAME')
SCOPE = 'playlist-modify-public'
REDIRECT_URI = "http://localhost/"


def spotify_auth():
	token = util.prompt_for_user_token(USERNAME, SCOPE, client_id=CLIENT_ID,client_secret=SECRET_ID,redirect_uri=REDIRECT_URI)
	if token: 
		return spotipy.Spotify(auth=token)
	else: 
		print("Can't get token for ", username)


def get_playlist_songs(spotify, playlist_id):
	""" Gets the tracks on the spotify playlist with audio analysis. """
	results = spotify.user_playlist(USERNAME, playlist_id)
	tracks = results['tracks']['items']
	track_ids = []
	for track in tracks:
		track_ids.append(track['track']['id'])
	songs = spotify.audio_features(tracks=track_ids)
	return songs


def score_songs(songs):
	""" Scores songs based on simple algo taking into account danceability, energy, and tempo. """
	scored_songs = {}
	for song in songs:
        # Can mess around with the scoring
		scored_songs[song['id']] = song['danceability'] + song['danceability'] + song['energy'] # * song['danceability'] * song['tempo'] * song['energy']
	return scored_songs	


def sort_songs(scored_songs):
	""" Sorts a dictionary of scored songs. """
	sorted_songs = []
	for song_id, score in scored_songs.items():
		i = 0
		while i < len(sorted_songs):
			if score < sorted_songs[i]['score']:
				break
			i += 1
		sorted_songs.insert(i, {'id': song_id, 'score': score})
	return sorted_songs


def replace_tracks(spotify, sorted_songs, playlist_id):
	""" Replaces the tracks in the playlist. """
	track_ids = []
	for song in sorted_songs:
		track_ids.append(song['id'])
	spotify.user_playlist_replace_tracks(USERNAME, playlist_id, track_ids)


def __main__():
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	logging.info("WELCOME TO THE SPOTIFY PLAYLIST SORTER")

	# Parse Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--id', help='the ID of the playlist in question', default='3p1r9pzmoONlUdtN5bhFdC')
	args = parser.parse_args()

	spotify = spotify_auth()
	songs = get_playlist_songs(spotify, args.id)
	scored_songs = score_songs(songs)
	sorted_songs = sort_songs(scored_songs)
	replace_tracks(spotify, sorted_songs, args.id)

__main__()
