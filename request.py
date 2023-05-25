# IMPORTS
import requests
import base64
import json
import requests
import numpy
from sklearn.decomposition import PCA
import pandas

# GLOBAL VARIABLES
client_id = 'ce7fc85dbeaa40588c0a73a324a7654b'
client_secret = '8388086841354dd4bada7a48dfe91b72'

# FUNCTIONS
# Retrieves and convert token for using at Spotify's API
def get_token() :
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}

    result = requests.post(url, headers = headers, data = data)

    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

# Gives token a usable format to use in headers when requesting from API
def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

# Retrieves infomation from API from several tracks with their spotify ID's separeted by a coma (max 50 spotify ID's)
def search_several_tracks(token, tracks):
    url = 'https://api.spotify.com/v1/tracks'
    headers = get_auth_header(token)
    query = f"?ids={tracks}"

    query_url = url + query

    result = requests.get(query_url, headers=headers)

    json_result = json.loads(result.content)

    print(json_result)

# Retrieves audio analysis from API from a single track
def audio_analysis(token, track_id):
    url = 'https://api.spotify.com/v1/audio-analysis/'
    headers = get_auth_header(token)
    query_url = url + track_id

    result = requests.get(query_url, headers = headers)

    json_result = json.loads(result.content)

    return json_result

# Retrieves information from API from a single track
def audio_information(token, track_id):
    url = 'https://api.spotify.com/v1/tracks/'
    headers = get_auth_header(token)
    query_url = url + track_id

    result = requests.get(query_url, headers = headers)

    json_result = json.loads(result.content)

    return json_result

# Returns a list whit general info from a track analysis (duration, loudness, tempo, time_signature, key, mode)
def creates_general_info(track_analysis):
    track = track_analysis["track"]
    general = [track["duration"], track["loudness"], track["tempo"], track["time_signature"], track["key"], track["mode"]]
    
    return general

# Returns pitches of each segment from a track analysis
def creates_pitches_info(track_analysis):
    pitches = []
    for segment in track_analysis["segments"] :
        pitches.append(segment["pitches"])

    return pitches

# Returns timbres of each segment from a track analysis
def creates_timbre_info(track_analysis):
    timbres = []
    for segment in track_analysis["segments"] :
        timbres.append(segment["timbre"])

    return timbres

# Applies PCA to a list of values returnins only 'components parameter' number of principal componentes
def pca(info, components) :
    pca = PCA(n_components=components)
    x = pca.fit_transform(info)

    return x

# Creates a single list concatenating general info, pitches_pca info and timbre_pca info
def concatenate_info(general, pitches, timbre):
    for pitch in pitches :
        general.append(pitch[0])

    for timbr in timbre :
        general.append(timbr[0])

    return general

# Processes a single track by their Spotify ID creating our usable analysis
def track_analysis(token, trackID):
    track_analysis = audio_analysis(token, trackID)

    track_data = concatenate_info(creates_general_info(track_analysis), pca(creates_pitches_info(track_analysis), 1), pca(creates_timbre_info(track_analysis), 1))

    return track_data

# MAIN
# Retrieves a token
token = get_token()

# Opens a .txt file containing track's spotify ID's *each track must end with a newline and the EOF is represented by a blank line* 
tracks = open('prueba.txt', 'r')

# Creates a dataframe to store tracks analysis
data_set = pandas.DataFrame()

# Creates a list to store song_name - artist_name
row_names = []

# Iterate over .txt file concatenating each track analysis and name - artist on data_set data frame
for track in tracks :
    track = str(track)
    track = track[:-1]

    aux = track_analysis(token, track)
    
    data_set = pandas.concat([data_set, pandas.DataFrame([aux])], axis = 0)
    

    track_information = audio_information(token, track)
    name = track_information["name"]
    band = track_information["artists"][0]["name"]

    new_row = f'{name} - {band}'
    row_names.append(new_row)

# Set song_name - artist_name as row indexes
data_set.index = row_names

# PROBLEM: PCA do not allow NaN values. Try to replace NaN values for something else
#final_data_set = pandas.DataFrame(pca(data_set, 5))

print(data_set)