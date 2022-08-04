import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spoti_functions as spoti

# get Spotipy Api Credentials (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT SECRET and SPOTIPY_REDIRECT_URI)
# and set as environmental variables

username = 'deszczowaa'
scope_playlist = 'playlist-modify-public'


if __name__ == "__main__":

    name = input("Name your playlist: ")
    description = input("Write a description: ")
    path = input("Write path to your csv file")

    # path = 'clustered/kmeans-3clusters/km1-cluster1.csv'
    token = SpotifyOAuth(scope=scope_playlist, username=username)
    sp = spotipy.Spotify(auth_manager=token)

    lists = spoti.get_songs_ids(path)

    spoti.create_playlist(sp, username, name, description, lists)
