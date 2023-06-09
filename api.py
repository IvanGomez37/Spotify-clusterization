import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

# Set your client ID and client secret obtained from the Spotify Developer Dashboard
client_id = (os.getenv('CLIENT_ID'))
client_secret = (os.getenv('CLIENT_SECRET'))

# Set the URI of the playlist you want to retrieve track IDs from
playlist_uri = 'https://open.spotify.com/playlist/6jLIBc4ja8Jf2DlobQB62D?si=fa5a9b34f7af4d97'

# Create an instance of the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Retrieve the playlist tracks
results = sp.playlist_tracks(playlist_uri)
tracks = results['items']

# Iterate through all tracks in the playlist
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Extract track IDs from the playlist tracks
track_ids = [track['track']['id'] for track in tracks]

# Print the track IDs

with open('out.txt', 'w') as output:
    for track_id in track_ids:
        output.write(track_id + '\n')
