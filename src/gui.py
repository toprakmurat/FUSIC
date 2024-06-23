from lyrics_ovh import get_all_lyrics_for_artist
from spotify_api import SpotifyAPI

import customtkinter as ctk
import tkinter as tk

import platform
import os
import re

import messages 

# TODO: Info messages/print statements should be visible to users
# TODO: A progress bar should be visible to users
# TODO: Improve error checking

# Supported platforms (Darwin: macOS)
PLATFORMS = ["Windows", "Linux", "Darwin"]

# Credentials
spotify_client_id = ''
spotify_client_secret = ''

# Helper function to replace invalid filenames with the new ones
def sanitize_filename(filename: str) -> str:
    current_os = platform.system()

    # Define invalid characters for each supported OS
    invalid_chars_windows = r'[<>:"/\\|?*\x00-\x1F]'
    invalid_chars_macos = r'[:]'
    invalid_chars_linux = r'[/\x00]'

    # Select the appropriate invalid characters regex based on the OS
    if current_os == 'Windows':
        invalid_chars = re.compile(invalid_chars_windows)
    elif current_os == 'Darwin':  # macOS
        invalid_chars = re.compile(invalid_chars_macos)
    elif current_os == 'Linux':
        invalid_chars = re.compile(invalid_chars_linux)

    else:
        raise messages.UnsupportedPlatformError(platform)
    
    # Replace invalid characters with '.'
    sanitized_filename = invalid_chars.sub('.', filename)

    # Truncate the filename to 255 characters
    if len(sanitized_filename) > 255:
        sanitized_filename = sanitized_filename[:255]

    return sanitized_filename

# Helper function to create files from tracks of an artist
def create_files(spotify_api: SpotifyAPI, directory: str, artist_name: str) -> bool:
    try:
        tracks = spotify_api.get_all_tracks(artist_name)
        for track in tracks:
        	pass

        lyrics_dict = get_all_lyrics_for_artist(artist_name, tracks)
        for track, lyrics in lyrics_dict.items():
            new_track_name = sanitize_filename(track)
            fpath = os.path.join(directory, f'{new_track_name}.txt') 
            with open(fpath, "w", encoding="utf-8") as file:
                file.write(f'{lyrics}')
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Helper function to create a directory
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

# Main Application Class
class FusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FUSIC")
        self.geometry("400x300")
        
        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = ctk.CTkLabel(self, text="FUSIC", font=("Arial", 20))
        self.title_label.pack(pady=20)

        # Artist label and entry
        self.artist_label = ctk.CTkLabel(self, text="Artist:")
        self.artist_label.pack(anchor=tk.W, padx=20)
        
        self.artist_entry = ctk.CTkEntry(self, placeholder_text="Enter an artist name:")
        self.artist_entry.pack(padx=20, pady=10, fill=tk.X)

        # Directory label and entry
        self.directory_label = ctk.CTkLabel(self, text="Directory:")
        self.directory_label.pack(anchor=tk.W, padx=20)
        
        self.directory_entry = ctk.CTkEntry(self, placeholder_text="Directory to save lyrics:")
        self.directory_entry.pack(padx=20, pady=10, fill=tk.X)

        # Download button
        self.download_button = ctk.CTkButton(self, text="Download", command=self.download)
        self.download_button.pack(pady=20)

    def download(self):
        # Logic to handle the download button click
        artist_name = self.artist_entry.get()
        directory = self.directory_entry.get()

        # Download logic
        if create_dir(directory):
            spotify_api = SpotifyAPI(spotify_client_id, spotify_client_secret)
            res = create_files(spotify_api, directory, artist_name)

# Running the app/
if __name__ == "__main__":
    app = FusicApp()
    app.mainloop()
