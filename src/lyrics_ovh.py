import requests

def get_lyrics(artist_name, track_name):
    base_url = f'https://api.lyrics.ovh/v1/{artist_name}/{track_name}'
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        return data.get('lyrics', 'Lyrics not found.')
    return 'Lyrics not found.'

def get_all_lyrics_for_artist(artist_name, tracks):
    all_lyrics = {}
    for track in tracks:
        lyrics = get_lyrics(artist_name, track)
        all_lyrics[track] = lyrics
    return all_lyrics
