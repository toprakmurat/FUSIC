from lyrics_ovh import get_all_lyrics_for_artist 
from spotify_api import SpotifyAPI


from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk

from typing import Callable, Any
import platform
import os
import re

import messages 

# Supported platforms (Darwin: macOS)
PLATFORMS = ["Windows", "Linux", "Darwin"]

# Credentials
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

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
def create_files(spotify_api: SpotifyAPI, directory: str, artist_name: str, 
    progress_callback: Callable[[Any, int], None]) -> bool:
    
    try:
        tracks = spotify_api.get_all_tracks(artist_name)
        total_tracks = len(tracks)
        for index, track in enumerate(tracks):
            # Update progress
            progress_callback((index + 1) / total_tracks)
            lyrics_dict = get_all_lyrics_for_artist(artist_name, [track])
            for track_name, lyrics in lyrics_dict.items():
                if lyrics == "Lyrics not found.":
                    continue
                new_track_name = sanitize_filename(track_name)
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

# Progress Window Class
class ProgressWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        master.withdraw()
        self.title("Progress")
        self.geometry("600x200")
        
        self.title_label = ctk.CTkLabel(self, text="Downloading...", font=("Arial", 20,"bold"))
        self.title_label.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, mode='determinate', width=500,height=40)
        self.progress_bar.pack(pady=20, padx=20, fill=tk.X)
        self.progress_bar.set(0)


    def update_progress(self, value: float) -> None:
        self.progress_bar.set(value)
        self.update_idletasks()

# Main Application Class
class FusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fusic")
        self.geometry("800x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=30)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.create_widgets()

    def create_label(self, master, text, fg_color=None, text_color=None, 
        font=("Ariel",15,"bold"), height=40, width=140, corner_radius=None, 
        image=None, padx=(0,0), pady=(0,0), fill=None, expand=None,anchor=tk.W
        ):

        label = ctk.CTkLabel(master, text=text, fg_color=fg_color, text_color=text_color, 
            font=font, height=height, width=width, corner_radius=corner_radius, image=image)
        label.pack(pady=pady, padx=padx, fill=fill, expand=expand, anchor=anchor)
        return label

    def create_entry(self, master, placeholder_text, height=40, padx=(0,0), pady=(0,0), fill=tk.X):
        entry = ctk.CTkEntry(master, placeholder_text=placeholder_text, height=height)
        entry.pack(padx=padx, pady=pady, fill=fill)
        return entry

    def create_widgets(self):
        # Image
        image = Image.open("../assets/fusic.png")
        image = image.resize((400, 400))
        
        # First frame
        self.frame_1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_1.grid(row=0, column=0, padx=(0,10), pady=(0, 0), sticky="nsw", rowspan=2)

        # Label to hold the image
        ctk_image = ctk.CTkImage(light_image=image,size=(400,400))
        self.image_label = self.create_label(self.frame_1, "", width=400, height=400, 
            image=ctk_image, fill=tk.BOTH, expand=True)
        
        # Second frame
        self.frame_2 = ctk.CTkFrame(self, fg_color="gray", corner_radius=20)
        self.frame_2.grid(row=0, column=1, padx=(0,15), pady=(10, 0), sticky="nsew")

        # Download button
        self.button = ctk.CTkButton(self, fg_color="lightgray", 
            text="Download", text_color="black", command=self.download)
        self.button.grid(row=1, column=1, padx=(0,15), pady=10, sticky="ew")

        # Title
        self.title_label = self.create_label(self.frame_2, "FUSIC", fg_color="lightgray", 
            text_color="black", font=("Arial", 25, "bold"), height=40, width=300, 
            corner_radius=25, pady=(20, 50),anchor=tk.CENTER)

        # Artist label and entry
        self.artist_label = self.create_label(self.frame_2, "Artist", fg_color="lightgray", 
            text_color="black", corner_radius=100,padx=(15,0))
        self.artist_entry = self.create_entry(self.frame_2, "Enter an artist name:", 
            pady=(10, 10),padx=(15,15))

        # Directory label and entry
        self.directory_label = self.create_label(self.frame_2, "Directory", fg_color="lightgray", 
            text_color="black", corner_radius=100,padx=(15,0))
        self.directory_entry = self.create_entry(self.frame_2, "Directory to save lyrics:", 
            pady=(10, 10),padx=(15,15))
    
        self.directory_entry.bind("<ButtonRelease>", self.select_and_display_path)
        
    def get_folder_path(self):
        folder_path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        return folder_path

    def select_and_display_path(self, event):
        path = self.get_folder_path()
        if path:
            self.directory_entry.delete(0, ctk.END)
            self.directory_entry.insert(0, path)

    def cleanup_window(self):
        self.deiconify()
        self.artist_entry.delete(0, ctk.END)
        self.directory_entry.delete(0, ctk.END)
        self.focus()

    def download(self):
        artist_name = self.artist_entry.get()
        directory = self.directory_entry.get()

        res = create_dir(directory)
        if not res:
            messagebox.showerror("Error", f"Failed to create directory {directory}")

        # Open progress window
        self.progress_window = ProgressWindow(self)
        self.after(100, self.start_download, artist_name, directory)

        # Start download process
    def start_download(self, artist_name: str, directory: str) -> None:
        spotify_api = SpotifyAPI(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
        success = create_files(spotify_api, directory, artist_name, self.progress_window.update_progress)
        
        self.progress_window.destroy()
        self.cleanup_window()
        if success:
            messagebox.showinfo("Success", "Lyrics downloaded successfully.")
        else:
            messagebox.showerror("Error", "Failed to download lyrics.")
