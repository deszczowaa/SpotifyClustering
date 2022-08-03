import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer


def elbow_method(data):
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

    model = KMeans(random_state=0)
    visualizer = KElbowVisualizer(model, k=(2, 15), metric='silhouette', timings=False)
    visualizer.fit(data_scaled)
    score1 = visualizer.elbow_score_
    value1 = visualizer.elbow_value_
    visualizer.show()
    return score1, value1, data_scaled


def kmeans_clustering(data, k, df_features, df_info):
    kmeans = KMeans(init="k-means++", n_clusters=k, random_state=15).fit(data)
    df_features[f'kmeans-{k}clusters'] = kmeans.labels_
    df_info[f'kmeans-{k}clusters'] = kmeans.labels_
    return df_features, df_info
