import pandas as pd
import glob


class CreatePlaylist:

    def __init__(self, sp, username, playlist_name):
        self.sp = sp
        self.username = username
        self.playlist_name = playlist_name

    def create_playlist(self):
        files = self._find_clusters(self.playlist_name)
        index = 1
        for file in files:
            name = f"Playlist {index} created from {self.playlist_name}"
            description = f"Result of clusterization of playlist {self.playlist_name} by kmeans algorithm"
            self._upload_songs(name, description, file)
            index += 1

    @staticmethod
    def _find_clusters(playlist_name):
        files = []
        for file in glob.glob(f"clustered{playlist_name}/cluster*.csv"):
            files.append(file)
        return files

    def _upload_songs(self, name, description, path):
        self.sp.user_playlist_create(user=self.username, name=name,
                                     public=True, collaborative=False,
                                     description=description)
        list_of_playlists = self.sp.user_playlists(user=self.username)
        playlist_id = list_of_playlists['items'][0]['id']
        lists = self._get_songs_ids(path)
        for songs in lists:
            self.sp.user_playlist_add_tracks(user=self.username, playlist_id=playlist_id, tracks=songs)
        print(f"Your songs have been added to the playlist {name}!")

    @staticmethod
    def _get_songs_ids(path):
        cluster = pd.read_csv(path).iloc[:, 1:]
        cluster_id_list = cluster['id'].tolist()

        listoflists = []
        index = 0

        while len(cluster_id_list) > 0:
            offset = 100
            if len(cluster_id_list) > offset:
                new_list = cluster_id_list[index:index+offset]
                cluster_id_list = cluster_id_list[index+offset:]
                listoflists.append(new_list)
            else:
                listoflists.append(cluster_id_list)
                cluster_id_list = []
        return listoflists
