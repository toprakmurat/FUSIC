from spotify_api import SpotifyAPI
from lyrics_ovh import get_all_lyrics_for_artist
import os

# TODO: GUI
# All print statements are for CLI for now, which is temporary
# These print statements should be shown to users in GUI later

# same for input statements

# A progress bar should be visible to users

# Improve error checking

def create_dir(directory: str) -> bool:
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
        return True
    except FileExistsError:
        print(f"Directory '{directory}' is not empty, contents will not be overwritten.")
        return True
    except OSError as error:
        print(f"Error creating directory '{directory}': {error}")
        return False


def create_files(spotify_api: SpotifyAPI, directory: str, artist_name: str) -> bool:
    try:
        tracks = spotify_api.get_all_tracks(artist_name)
        for track in tracks:
            print(track)
        lyrics_dict = get_all_lyrics_for_artist(artist_name, tracks)
        for track, lyrics in lyrics_dict.items():
            fpath = os.path.join(directory, f'{track}.txt') 
            with open(fpath, "w") as file:
                file.write(f'{lyrics}')
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


if __name__ == '__main__':
    # Credentials
    spotify_client_id = ''
    spotify_client_secret = ''

    artist_name = input("Artist name: ")
    directory = input("Directory to save lyrics: ")

    if create_dir(directory):
        spotify_api = SpotifyAPI(spotify_client_id, spotify_client_secret)
        res = create_files(spotify_api, directory, artist_name)
