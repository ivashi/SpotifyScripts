import argparse
import logging
import os
import pprint
import sys

# Package Specific
from spotify_util import do_spotify_auth


def get_playlist_songs(username, spotify, playlist_id):
	""" Gets the tracks on the spotify playlist with audio analysis. """
	results = spotify.user_playlist(username, playlist_id)
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


def replace_tracks(username, spotify, sorted_songs, playlist_id):
	""" Replaces the tracks in the playlist. """
	track_ids = []
	for song in sorted_songs:
		track_ids.append(song['id'])
	spotify.user_playlist_replace_tracks(username, playlist_id, track_ids)


def __main__():
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	logging.info("WELCOME TO THE SPOTIFY PLAYLIST SORTER")

	# Parse Arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--id', help='the ID of the playlist in question', default='3p1r9pzmoONlUdtN5bhFdC')
	parser.add_argument('--username', help='username of individual who owns playlist', default='ivashishta')
	args = parser.parse_args()

	username = args.username

	spotify = do_spotify_auth(username)
	songs = get_playlist_songs(username, spotify, args.id)
	scored_songs = score_songs(songs)
	sorted_songs = sort_songs(scored_songs)
	replace_tracks(username, spotify, sorted_songs, args.id)

__main__()
