import pandas as pd
import json
import os


class DownloadPlaylist:
    def __init__(self, sp, username, playlist_name):
        self.sp = sp
        self.username = username
        self.playlist_name = playlist_name

    def get_playlist(self):
        offset = 0
        songs = []
        playlist_id = self._get_playlist_id(self.playlist_name)
        while True:
            playlist = self.sp.user_playlist_tracks(self.username, playlist_id, limit=10, offset=offset)
            songs += playlist['items']
            if playlist['next'] is not None:
                offset += 10
            else:
                break

        os.mkdir(f'clustered{self.playlist_name}')
        with open(f'clustered{self.playlist_name}playlist', 'w') as outfile:
            json.dump(songs, outfile)

        info_file = self._get_playlist_songs_info(songs)
        features_file = self._get_playlist_audio_features(songs)
        return songs, info_file, features_file

    def _get_playlist_id(self, name):
        list_of_playlists = self.sp.user_playlists(user=self.username)
        for playlist in list_of_playlists['items']:
            if name == playlist['name']:
                playlist_id = playlist['id']
                return playlist_id

    def _get_playlist_songs_info(self, songs):
        info = []
        df_info = pd.DataFrame(info, columns=['name', 'album', 'artist',
                                              'release_date', 'duration',
                                              'popularity', 'id'])

        for song in songs:
            inf = self.sp.track(song['track']['id'])
            info.append([inf['name'], inf['album']['name'],
                         inf['album']['artists'][0]['name'],
                         inf['album']['release_date'], inf['duration_ms'],
                         inf['popularity'], inf['id']])
            df_info = pd.DataFrame(info, columns=['name', 'album', 'artist',
                                                  'release_date', 'duration',
                                                  'popularity', 'id'])

        # print(df_info)
        df_info.to_csv(f'clustered{self.playlist_name}/songs_info.csv')
        info_file = 'songs_info.csv'
        return info_file

    def _get_playlist_audio_features(self, songs):
        audio_features = []
        df_features = pd.DataFrame(audio_features, columns=['energy', 'liveness',
                                                            'tempo', 'speechiness',
                                                            'acousticness', 'instrumentalness',
                                                            'time_signature', 'danceability',
                                                            'key', 'duration_ms', 'loudness',
                                                            'valence', 'mode', 'type', 'uri'])

        for song in songs:
            features = self.sp.audio_features(song['track']['id'])
            audio_features.append([features[0]['energy'], features[0]['liveness'],
                                   features[0]['tempo'], features[0]['speechiness'],
                                   features[0]['acousticness'], features[0]['instrumentalness'],
                                   features[0]['time_signature'], features[0]['danceability'],
                                   features[0]['key'], features[0]['duration_ms'],
                                   features[0]['loudness'], features[0]['valence'],
                                   features[0]['mode'], features[0]['type'],
                                   features[0]['uri']])
            df_features = pd.DataFrame(audio_features, columns=['energy', 'liveness',
                                                                'tempo', 'speechiness',
                                                                'acousticness', 'instrumentalness',
                                                                'time_signature', 'danceability',
                                                                'key', 'duration_ms', 'loudness',
                                                                'valence', 'mode', 'type', 'uri'])

        # print(df_features)
        df_features.to_csv(f'clustered{self.playlist_name}/audio_features.csv')
        features_file = 'audio_features.csv'
        return features_file
