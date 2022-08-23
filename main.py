import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

from download_playlist import DownloadPlaylist
from cluster_playlist import ClusterPlaylist
from create_playlist import CreatePlaylist


# get Spotipy Api Credentials (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT SECRET and SPOTIPY_REDIRECT_URI)
# and set as environmental variables

if __name__ == "__main__":

    username = input("Username: ")
    playlist_name = input("Which playlist would you like to cluster? Write name:  ")

    # starts spotipy session
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # downloads users playlist from Spotify
    playlist = DownloadPlaylist(sp, username, playlist_name)
    songs, info_file, features_file = playlist.get_playlist()

    # clusters the playlist into groups
    cluster = ClusterPlaylist(info_file, features_file, playlist_name)
    cluster.cluster_data()

    token = SpotifyOAuth(scope='playlist-modify-public', username=username)
    sp = spotipy.Spotify(auth_manager=token)

    # creates new playlists out of clustered groups
    playlist = CreatePlaylist(sp, username, playlist_name)
    playlist.create_playlist()
