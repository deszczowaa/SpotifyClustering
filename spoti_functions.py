import pandas as pd
import json


def get_playlist(sp, username, playlist_id):
    offset = 0
    songs = []
    while True:
        playlist = sp.user_playlist_tracks(username, playlist_id, limit=10, offset=offset)
        songs += playlist['items']
        if playlist['next'] is not None:
            offset += 10
        else:
            break

    with open('playlist', 'w') as outfile:
        json.dump(songs, outfile)
    return songs


def get_playlist_songs_info(sp, songs):

    info = []
    df_info = pd.DataFrame(info, columns=['name', 'album', 'artist',
                                          'release_date', 'duration',
                                          'popularity', 'id'])

    for song in songs:
        inf = sp.track(song['track']['id'])
        info.append([inf['name'], inf['album']['name'],
                     inf['album']['artists'][0]['name'],
                     inf['album']['release_date'], inf['duration_ms'],
                     inf['popularity'], inf['id']])
        df_info = pd.DataFrame(info, columns=['name', 'album', 'artist',
                                              'release_date', 'duration',
                                              'popularity', 'id'])

    # print(df_info)
    df_info.to_csv('songs_info.csv')
    return df_info


def get_playlist_audio_features(sp, songs):
    audio_features = []
    df_features = pd.DataFrame(audio_features, columns=['energy', 'liveness',
                                                        'tempo', 'speechiness',
                                                        'acousticness', 'instrumentalness',
                                                        'time_signature', 'danceability',
                                                        'key', 'duration_ms', 'loudness',
                                                        'valence', 'mode', 'type', 'uri'])

    for song in songs:
        features = sp.audio_features(song['track']['id'])
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
    df_features.to_csv('audio_features.csv')
    return df_features
