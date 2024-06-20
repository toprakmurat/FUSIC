import customtkinter as ctk
from tkinter import filedialog
import time

# TODO: organizing the variables and their names
# TODO: avoid hardcoding as much as possible

# TODO: implement the bridge between the app and the GUI
# TODO: organize the functions, some of them does not need to be inside the class
# TODO: Write type annotations for the functions

class FusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Creating the main window of the FUSIC app
        self.__initialize_window()
        self.__create_widgets()
        self.__layout_widgets()
        
    def __initialize_window(self):
        # TODO: implement error checking for the parameters
        title = "FUSIC"
        window_width = 750
        window_height = 600
        app_mode = 'dark'

        self.title(f"{title}")
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        ctk.set_appearance_mode(f"{app_mode}")

    def __create_widgets(self):
        # TODO: classifying messages
        # TODO: making variables more organized

        artist_err_txt = "You must enter the name of the artist"
        dir_err_txt    = "You must choose where you want to upload it"

        artist_ent_txt = "Enter an artist name: "
        dir_ent_txt    = "Directory to save lyrics: "

        # Crating the main frame
        self.__main_window = ctk.CTkFrame(self, fg_color=("gray15", "gray25"), corner_radius=8)

        # Labels
        self.__error_label_artist    = ctk.CTkLabel(self.__main_window, text=artist_err_txt, text_color="red")
        self.__error_label_directory = ctk.CTkLabel(self.__main_window, text=dir_err_txt, text_color="red")
        self.__label1 = ctk.CTkLabel(self.__main_window, text="Music Downloader", corner_radius=10,
                                    font=("Calibri", 35, "bold"), text_color="white")
        self.__label2 = ctk.CTkLabel(self.__main_window, text="Artist:", corner_radius=10, 
                                    font=("Calibri", 20, "bold"), text_color="white")
        self.__label3 = ctk.CTkLabel(self.__main_window, text="Directory:", corner_radius=10, 
                                    font=("Calibri", 20, "bold"), text_color="white")

        # Entries
        self.__artist_entry = ctk.CTkEntry(self.__main_window, 
                        placeholder_text=artist_ent_txt, width=410, height=40)
        self.__dir_entry = ctk.CTkEntry(self.__main_window, 
                        placeholder_text=dir_ent_txt, width=410, height=40)
        self.__dir_entry.bind("<ButtonRelease>", self.__select_and_display_path)
        self.__button = ctk.CTkButton(self.__main_window, text="Download", fg_color="darkgray", 
                    text_color="Black", command=self.__clicked, width=160, height=40, font=("Ariel", 18))

    def __layout_widgets(self):
        self.__main_window.pack(pady=40, padx=80, fill="both", expand=True)
        self.__main_window.grid_columnconfigure(0, weight=1)

        for i in range(7):
            self.__main_window.grid_rowconfigure(i, weight=1)
        
        self.__label1.grid(row=0, column=0)
        self.__label2.grid(row=1, column=0, sticky="ws", padx=83)
        self.__label3.grid(row=3, column=0, sticky="ws", padx=83)
        self.__artist_entry.grid(column=0, row=2, pady=(0, 10))
        self.__dir_entry.grid(column=0, row=4)
        self.__button.grid(column=0, row=5, pady=(15, 0))

    def __get_folder_path(self):
        folder_path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        return folder_path

    def __select_and_display_path(self, event):
        path = self.__get_folder_path()
        if path:
            self.__dir_entry.delete(0, ctk.END)
            self.__dir_entry.insert(0, path)

    # Helper function to close a window
    def __close_progress_window(self, window):
        window.destroy()

    # Helper function to update a progress bar when needed
    def __update_prog_bar(self, progress_bar, total_dwn: int, dwn_num: int, dwn_time: float) -> None:
        time.sleep(dwn_time)
        progress_bar.set(dwn_num / total_dwn)  # setting forward
        progress_bar.update()

    def __cleanup_window(self):
        self.deiconify()
        self.__artist_entry.delete(0, ctk.END)
        self.__dir_entry.delete(0, ctk.END)
        self.__error_label_artist.grid_forget()
        self.__error_label_directory.grid_forget()
        self.focus()

    def __progress_bar(self, dwn_window):
        # Setting up the progress bar
        progress_label = ctk.CTkLabel(dwn_window, text="Downloading...", corner_radius=8, font=("Ariel", 25, "bold"))
        progress_label._set_appearance_mode("light")
        progress_label.pack(pady=60)
        progress_bar = ctk.CTkProgressBar(dwn_window, width=400, height=20, mode="determinate")
        progress_bar._set_appearance_mode("light")
        progress_bar.pack(pady=10)

        progress_bar.set(0)

        return progress_bar

    def __download_window(self, total_dwn):
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
    
    def __is_empty(self):
        empty = False
        if not self.__artist_entry.get():
            self.__error_label_artist.grid(column=0, row=6,sticky= "s",pady= (0,5))
            empty = True
        else:
            self.__error_label_artist.grid_forget()
            

        if not self.__dir_entry.get():
            self.__error_label_directory.grid(column=0, row=7,sticky = "n",pady=(0,5))
            empty = True
        else:
            self.__error_label_directory.grid_forget()
            

        return empty


    def __clicked(self):
        # TODO: get the total number of tracks based on user's choice
        self.__total_tracks = 10  # temporarily, debugging purposes
        duration = 0.25  # temporarily, debugging purposes

        if self.__is_empty():
            return

        self.__name_of_artist = self.__artist_entry.get()
        self.__path_of_directory = self.__dir_entry.get()

        # Initialize Download window and progress bar
        dwn_window = self.__download_window(self.__total_tracks)
        progress_bar = self.__progress_bar(dwn_window)
        
        # Updating progress bar
        for i in range(self.__total_tracks):
            self.__update_prog_bar(progress_bar, self.__total_tracks, i,duration)

        dwn_window.after(1000, self.__close_progress_window(dwn_window))
        self.__cleanup_window()

        def get_name_of_artist(self):
            return self.__name_of_artist
        
        def get_path_of_directory(self):
            return self.__path_of_directory

        def set_total_tracks(self,total_tracks):
            self.__total_tracks = total_tracks

        

# Running the app
# if __name__ == "__main__":
#     app = FusicApp()
#     app.mainloop()
