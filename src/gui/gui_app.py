from tkinter import filedialog

import customtkinter as ctk
import time

# TODO: organizing the variables and their names
# TODO: avoid hardcoding as much as possible

# TODO: implement the bridge between the app and the GUI
# TODO: organize the functions, some of them does not need to be inside the class
# TODO: Write type annotations for the functions

class FusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Attributes for main window
        self.mw_title = "FUSIC"    # default
        self.mw_app_mode = "dark"  # default
        self.mw_window_width  = 0
        self.mw_window_height = 0

        # Private Attributes
        self._artist       = ""
        self._install_path = ""
        self._total_tracks = 0

        # Creating the main window of the FUSIC app
        self.initialize_window(750, 600)
        self.create_widgets()
        self.layout_widgets()

    @property
    def total_tracks(self):
        return self._total_tracks
    
    @total_tracks.setter
    def total_tracks(self, value):
        if total_tracks < 0:
            raise ValueError("Tracks could not be less than 0")
        self._total_tracks = value

    @property
    def install_path(self):
        return self._install_path
    
    @install_path.setter
    def install_path(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid Install Path: Installation path must be a 'str'")
        self._install_path = value

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        # TODO: Check if artist name available or not
        if not isinstance(value, str):
            raise ValueError("Invalid Artist Name: artist name must be a 'str'")
        self._artist = value
    
    def initialize_window(self, width, height):
        if width < 0 or height < 0:
            raise ValueError("Invalid values for the arguments width and/or height")

        self.mw_window_width  = width
        self.mw_window_height = height

        self.title(f"{self.mw_title}")
        self.geometry(f"{self.mw_window_width}x{self.mw_window_height}")
        self.resizable(False, False)
        ctk.set_appearance_mode(f"{self.mw_app_mode}")

    def create_widgets(self):
        # TODO: classifying messages
        # TODO: making variables more organized

        artist_err_txt = "You must enter the name of the artist"
        dir_err_txt    = "You must choose where you want to upload it"

        artist_ent_txt = "Enter an artist name: "
        dir_ent_txt    = "Directory to save lyrics: "

        # Crating the main window
        self.main_window = ctk.CTkFrame(self, fg_color=("gray15", "gray25"), corner_radius=8)

        # Labels
        self.error_label_artist    = ctk.CTkLabel(self.main_window, text=artist_err_txt, text_color="red")
        self.error_label_directory = ctk.CTkLabel(self.main_window, text=dir_err_txt, text_color="red")
        self.label1 = ctk.CTkLabel(self.main_window, text="Music Downloader", corner_radius=10,
                                    font=("Calibri", 35, "bold"), text_color="white")
        self.label2 = ctk.CTkLabel(self.main_window, text="Artist:", corner_radius=10, 
                                    font=("Calibri", 20, "bold"), text_color="white")
        self.label3 = ctk.CTkLabel(self.main_window, text="Directory:", corner_radius=10, 
                                    font=("Calibri", 20, "bold"), text_color="white")

        # Entries
        self.artist_entry = ctk.CTkEntry(self.main_window, 
                        placeholder_text=artist_ent_txt, width=410, height=40)
        self.dir_entry = ctk.CTkEntry(self.main_window, 
                        placeholder_text=dir_ent_txt, width=410, height=40)
        self.dir_entry.bind("<ButtonRelease>", self.select_and_display_path)
        self.button = ctk.CTkButton(self.main_window, text="Download", fg_color="darkgray", 
                    text_color="Black", command=self.clicked, width=160, height=40, font=("Ariel", 18))

    def layout_widgets(self):
        self.main_window.pack(pady=40, padx=80, fill="both", expand=True)
        self.main_window.grid_columnconfigure(0, weight=1)

        for i in range(7):
            self.main_window.grid_rowconfigure(i, weight=1)
        
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0, sticky="ws", padx=83)
        self.label3.grid(row=3, column=0, sticky="ws", padx=83)
        self.artist_entry.grid(column=0, row=2, pady=(0, 10))
        self.dir_entry.grid(column=0, row=4)
        self.button.grid(column=0, row=5, pady=(15, 0))

    def select_and_display_path(self, event):
        # Get installation path and check if it exists
        path = filedialog.askdirectory(initialdir='/', title="Select a directory")
        if path:
            self.dir_entry.delete(0, ctk.END)
            self.dir_entry.insert(0, path)

    # Helper function to close a window
    def close_progress_window(self, window):
        window.destroy()

    # Helper function to update a progress bar when needed
    def update_prog_bar(self, progress_bar, total_dwn: int, dwn_num: int, dwn_time: float) -> None:
        time.sleep(dwn_time)
        progress_bar.set(dwn_num / total_dwn)  # setting forward
        progress_bar.update()

    def cleanup_window(self):
        self.deiconify()
        self.artist_entry.delete(0, ctk.END)
        self.dir_entry.delete(0, ctk.END)
        self.error_label_artist.grid_forget()
        self.error_label_directory.grid_forget()
        self.focus()

    def progress_bar(self, dwn_window):
        # Setting up the progress bar
        progress_label = ctk.CTkLabel(dwn_window, text="Downloading...", corner_radius=8, font=("Ariel", 25, "bold"))
        progress_label._set_appearance_mode("light")
        progress_label.pack(pady=60)
        progress_bar = ctk.CTkProgressBar(dwn_window, width=400, height=20, mode="determinate")
        progress_bar._set_appearance_mode("light")
        progress_bar.pack(pady=10)

        progress_bar.set(0)

        return progress_bar

    def download_window(self, total_dwn):
        # TODO: implement error checking for the parameters
        title = "Downloading"
        window_width = 600
        window_height = 400
        app_mode = 'light'

        self.withdraw()
        # Setting up the main download window
        dwn_window = ctk.CTkToplevel(self)
        dwn_window.title(f"{title}")
        dwn_window.resizable(False, False)
        dwn_window.geometry(f"{window_width}x{window_height}")
        dwn_window._set_appearance_mode(f"{app_mode}")

        return dwn_window

    def clicked(self):
        # TODO: get the total number of tracks based on user's choice
        total_tracks = 10  # temporarily, debugging purposes
        duration = 0.25  # temporarily, debugging purposes

        if not self.artist_entry.get():
            self.error_label_artist.grid(column=0, row=6)
            return

        if not self.dir_entry.get():
            self.error_label_directory.grid(column=0, row=6)
            return

        name_of_artist = self.artist_entry.get()
        path_of_directory = self.dir_entry.get()

        self._install_path = path_of_directory
        self._artist = name_of_artist

        # Initialize Download window and progress bar
        dwn_window = self.download_window(total_tracks)
        progress_bar = self.progress_bar(dwn_window)
        
        # Updating progress bar
        for i in range(total_tracks):
            self.update_prog_bar(progress_bar, total_tracks, i, duration)

        dwn_window.after(1000, self.close_progress_window(dwn_window))
        self.cleanup_window()

# Running the app
if __name__ == "__main__":
    app = FusicApp()
    app.mainloop()
