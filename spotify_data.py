import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spoti_functions as spoti

# get Spotipy Api Credentials (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT SECRET)
# and set as environmental variables

# spotify username and playlist_id
username = 'deszczowaa'
playlist_id = '5i0gzjzuAaIB5GG0zUOPkQ'

if __name__ == "__main__":

    # start spotipy session
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    songs = spoti.get_playlist(sp, username, playlist_id)

    df_info = spoti.get_playlist_songs_info(sp, songs)

    df_features = spoti.get_playlist_audio_features(sp, songs)




