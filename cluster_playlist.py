import os

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer
import pandas as pd
import seaborn as sns
import plotly.express as px


class ClusterPlaylist:
    def __init__(self, file1, file2, playlist_name):
        self.file1 = file1
        self.file2 = file2
        self.playlist_name = playlist_name

    def cluster_data(self):
        # load playlist
        df_info = pd.read_csv(self.file1).iloc[:, 1:]
        df_features = pd.read_csv(self.file2).iloc[:, 1:]

        df_features = df_features.replace('spotify:track:', '', regex=True)

        # get binary values for categorical data
        for col in ['time_signature', 'key', 'mode']:
            dummies = pd.get_dummies(df_features[col], prefix=col)
            df_features = pd.concat([df_features, dummies], axis=1)
            df_features.drop(col, axis=1, inplace=True)

        # choose only columns with relevant features
        df1 = df_features.iloc[:, :10]
        # print(df1)
        # print(df1.describe())
        self._correlation(df1)
        score, k, df1_scaled = self._elbow_method(df1)
        features, info = self._kmeans_clustering(df1_scaled, k, df1, df_info)
        self._features_distribution(features, k)
        self._clusters_3d(info, features, k)
        self._save_data(info, features, k, self.playlist_name)

    @staticmethod
    def _correlation(data):
        # Pearson correlation matrix
        plt.figure(figsize=(10, 8))
        corr = data.corr()
        sns.heatmap(corr, annot=True)
        plt.title('Correlation between features', fontsize=16)
        plt.savefig('correlation_of_the_features.png')
        plt.show()

    @staticmethod
    def _elbow_method(data):
        # set parameters for kmeans
        min_max_scaler = MinMaxScaler()
        data_scaled = min_max_scaler.fit_transform(data)
        sum_of_squared_distances = []
        k_range = range(1, 15)
        for k in k_range:
            km = KMeans(n_clusters=k)
            km = km.fit(data_scaled)
            sum_of_squared_distances.append(km.inertia_)

        plt.plot(k_range, sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum_of_squared_distances')
        plt.title('Elbow Method For Optimal k')
        plt.show()

        model = KMeans(random_state=15)
        visualizer = KElbowVisualizer(model, k=(2, 15), metric='calinski_harabasz', timings=False)
        visualizer.fit(data_scaled)
        score = visualizer.elbow_score_
        value = visualizer.elbow_value_
        visualizer.show()
        return score, value, data_scaled

    @staticmethod
    def _kmeans_clustering(data, k, df_features, df_info):
        # perform kmeans for the playlist
        kmeans = KMeans(init="k-means++", n_clusters=k, random_state=15).fit(data)
        df_features[f'kmeans-{k}clusters'] = kmeans.labels_
        df_info[f'kmeans-{k}clusters'] = kmeans.labels_
        return df_features, df_info

    @staticmethod
    def _save_data(df_info, df_features, k, playlist_name):
        # save clusters to csvs
        os.mkdir(f'clustered{playlist_name}')
        for num in range(0, k):
            f1 = open('clustered' + playlist_name + '/cluster' + str(num) + ".csv", "w", encoding="utf-8")
            df_info[df_info[f'kmeans-{k}clusters'] == num].to_csv(f1, header=True)
            f2 = open('clustered' + playlist_name + '/features-cluster' + str(num) + ".csv", "w", encoding="utf-8")
            df_features[df_features[f'kmeans-{k}clusters'] == num].to_csv(f2, header=True)

    @staticmethod
    def _clusters_3d(df_info, df_features, k):
        # plot 3d visualisation of clusters
        fig = px.scatter_3d(df_features, x='acousticness', y='loudness', z='valence',
                            color=df_features[f'kmeans-{k}clusters'],
                            labels={f"kmeans-{k}clusters": "Clusters"},
                            title='Cluster division',
                            width=1000, height=800)
        fig.update_layout(
            margin=dict(
                l=50,
                r=50,
                b=50,
                t=50,
                pad=4))
        fig.show()
        fig.write_image('Clusters-visualisation.png')

        # plot 3d visualisation for each cluster
        for num in range(0, k):
            fig = px.scatter_3d(df_features[df_features[f'kmeans-{k}clusters'] == num], x='acousticness', y='loudness',
                                z='valence', color=df_info[df_info[f'kmeans-{k}clusters'] == num][f'kmeans-{k}clusters'],
                                text=df_info[df_info[f'kmeans-{k}clusters'] == num]['name'],
                                labels={
                                    "color": "Cluster-label"
                                },
                                title=f"Cluster {num} - songs",
                                width=1000, height=800)
            fig.update_layout(
                margin=dict(
                    l=50,
                    r=50,
                    b=50,
                    t=50,
                    pad=4))
            fig.show()
            fig.write_image(f'Cluster{num}songs.png')

    @staticmethod
    def _features_distribution(df_features, k):
        # only relevant columns from features table
        df = df_features.loc[:, ['energy', 'loudness', 'instrumentalness', "valence",
                                 "acousticness", "danceability", f"kmeans-{k}clusters"]]
        f, axes = plt.subplots(k, 1, figsize=(8, 6))
        for num in range(0, k):
            # limit the table to records classified as cluster
            x = df[df[f"kmeans-{k}clusters"] == num]
            x = x.drop([f'kmeans-{k}clusters'], axis=1)

            x = x.values  # return a numpy array
            min_max_scaler = MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            x = pd.DataFrame(x_scaled)
            x.columns = ['energy', 'loudness', 'instrumentalness', "valence", "acousticness", "danceability"]
            x = x.melt(var_name='Features', value_name=f'Cluster {num}')
            ax = sns.violinplot(data=x, x="Features", y=f"Cluster {num}", linewidth=0.6,
                                inner='point', scale='width', ax=axes[num])
            if num == 0:
                ax.set_title("Feature disribution across clusters", fontsize=16)
        plt.savefig('Features-distribution-across-clusters.png')
        plt.show()
