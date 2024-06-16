import requests

# TODO: error handling for requests

class SpotifyAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.spotify.com/v1'
        self.access_token = self.get_access_token()

    def get_access_token(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })

        auth_response_data = auth_response.json()
        return auth_response_data['access_token']

    def get_artist_id(self, artist_name):
        url = f'{self.base_url}/search'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        artists = response.json()['artists']['items']
        if artists:
            return artists[0]['id']
        return None

    def get_all_tracks(self, artist_name):
        artist_id = self.get_artist_id(artist_name)
        if not artist_id:
            raise Exception(f"Artist '{artist_name}' not found.")

        tracks = set()
        albums_url = f'{self.base_url}/artists/{artist_id}/albums'
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'include_groups': 'album,single',
            'limit': 50  # max limit is 50 for this program
        }
        response = requests.get(albums_url, headers=headers, params=params)
        response.raise_for_status()
        albums = response.json()['items']

        for album in albums:
            album_id = album['id']
            album_tracks_url = f'{self.base_url}/albums/{album_id}/tracks'
            response = requests.get(album_tracks_url, headers=headers)
            response.raise_for_status()
            album_tracks = response.json()['items']
            for track in album_tracks:
                track_name = track['name']
                if " - " not in track_name and "(" not in track_name:  # Filter out tracks with specific versions
                    tracks.add(track_name)

        return list(tracks)

