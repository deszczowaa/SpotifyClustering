import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import os

from download_playlist import DownloadPlaylist
from cluster_playlist import ClusterPlaylist
from create_playlist import CreatePlaylist
from create_report import PDF


# get Spotipy Api Credentials (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT SECRET and SPOTIPY_REDIRECT_URI)
# and set as environmental variables

if __name__ == "__main__":
    os.environ['SPOTIPY_CLIENT_ID'] = "ac6fd439e91046509cb6297fffe57586"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "9882a9f65c7b42a79dfc6af5ed68ff5b"
    os.environ['SPOTIPY_REDIRECT_URI'] = "http://127.0.0.1:8080/"

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

    # generates PDF report
    pdf = PDF(playlist_name)
