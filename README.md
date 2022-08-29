# SpotifyClustering

## The Spotify Clustering Project includes
- downloading playlist
- clusterization of playlist using k-means algorithm
- creating new playlists
- generating PDF report

Project was written with Python.

### Downloading and creating playlist
[Downloading](https://github.com/deszczowaa/SpotifyClustering/blob/master/download_playlist.py) and [creating](https://github.com/deszczowaa/SpotifyClustering/blob/master/create_playlist.py) new playlist was done with the use of spotipy library. The connection was established by getting Spotipy Credentials.

#### Getting Spotify Credentials
1. Visit [Spotify for Developers](https://developer.spotify.com/dashboard/login).
2. Log in using your Spotify account
3. Click the CREATE AN APP button. Add random name and description to your app.
4. Go to yor app and find the Client ID and Client Secret under the name of your app. Copy and save these credentials.
5. Click the EDIT SETTINGS button. Under Redirect URIs add: http://127.0.0.1:8080/ . Remember to save changes.
6.  In order to run the SpotifyClustering set environmental variables: SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI including the credentials from the previous steps.
7. Run the [script](https://github.com/deszczowaa/SpotifyClustering/blob/master/main.py) and follow the instructions. 

### K-means clusterization

Clusterization of playlist is performed based on features provided by Spotify. In this reasarch two approaches have been carried out:
- [automatic clustering](https://github.com/deszczowaa/SpotifyClustering/blob/master/k-means-clustering.ipynb) - divides playlist into few groups in a default way (based on k-means and elbow method for setting k value)
- [mood clustering](https://github.com/deszczowaa/SpotifyClustering/blob/master/mood-based-clustering.ipynb) - uses only a limited set of features in order to form two groups based on the feelings they indicate - energetic vs melancholic

In the main script the [first approach](https://github.com/deszczowaa/SpotifyClustering/blob/master/cluster_playlist.py) is used in order to form few playlist out of the original one.

### Generating PDF report
The results of clusterization can be viewed in [PDF report](https://github.com/deszczowaa/SpotifyClustering/blob/master/Clustering-report.pdf) generated at the end of the procedure. Moreover, in the [results folder](https://github.com/deszczowaa/SpotifyClustering/tree/master/clusteredLevel22) the generated lists of songs can be found.

A dockerized version made with Flask will be available on my github shortly.
