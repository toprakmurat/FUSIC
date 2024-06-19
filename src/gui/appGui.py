import customtkinter as ctk
from tkinter import filedialog
import time

# TODO: organizing the variables and their names
# TODO: avoid hardcoding as much as possible

# TODO: implement the bridge between the app and the GUI
FONT_FAMILY = "Calibri"

class FusicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Creating the main window of the FUSIC app
        self.initialize_window()
        self.create_widgets()
        self.layout_widgets()
        
    def initialize_window(self):
        # TODO: implement error checking for the parameters
        title = "FUSIC"
        window_width = 750
        window_height = 500
        app_mode = 'dark'

        self.title(title)
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        ctk.set_appearance_mode(app_mode)
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
                                    font=(f"{FONT_FAMILY}", 35, "bold"), text_color="white")
        self.label2 = ctk.CTkLabel(self.main_window, text="Artist:", corner_radius=10, 
                                    font=(f"{FONT_FAMILY}", 20, "bold"), text_color="white")
        self.label3 = ctk.CTkLabel(self.main_window, text="Directory:", corner_radius=10, 
                                    font=(f"{FONT_FAMILY}", 20, "bold"), text_color="white")

        # Entries
        self.artist_entry = ctk.CTkEntry(self.main_window, 
                        placeholder_text=artist_ent_txt, width=410, height=40)
        self.dir_entry = ctk.CTkEntry(self.main_window, 
                        placeholder_text=dir_ent_txt, width=410, height=40)
        self.dir_entry.bind("<ButtonRelease>", self.select_and_display_path)
        self.button = ctk.CTkButton(self.main_window, text="Download", fg_color="darkgray", 
                    text_color="Black", command=self.clicked, width=160, height=40, font=(f"{FONT_FAMILY}", 18))
        
    def layout_widgets(self):
        self.main_window.pack(pady=40, padx=80, fill="both", expand=True)
        self.main_window.grid_columnconfigure(0, weight=1)

        for i in range(8):
            self.main_window.grid_rowconfigure(i, weight=1)
        
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0, sticky="ws", padx=83)
        self.label3.grid(row=3, column=0, sticky="ws", padx=83)
        self.artist_entry.grid(column=0, row=2, pady=(0, 10))
        self.dir_entry.grid(column=0, row=4)
        self.button.grid(column=0, row=5, pady=(15, 0))
        
    def get_folder_path(self):
        folder_path = filedialog.askdirectory(initialdir="/", title="Select a directory")
        return folder_path

    def select_and_display_path(self, event):
        path = self.get_folder_path()
        if path:
            self.dir_entry.delete(0, ctk.END)
            self.dir_entry.insert(0, path)

    def close_progress_window(self, window):
        window.destroy()

    def download_window(self):
        self.withdraw()
        dwn_window = ctk.CTkToplevel(self)
        dwn_window.title("Downloading")
        dwn_window.resizable(False, False)
        dwn_window.geometry("600x400")

        dwn_window._set_appearance_mode("light")

        progress_label = ctk.CTkLabel(dwn_window, text="Downloading...", corner_radius=8, font=("Ariel", 25, "bold"))
        progress_label._set_appearance_mode("light")
        progress_label.pack(pady=60)

        progress_bar = ctk.CTkProgressBar(dwn_window, width=400, height=20, mode="determinate")
        progress_bar._set_appearance_mode("light")
        progress_bar.pack(pady=10)

        progress_bar.set(0)

        for i in range(201):
            time.sleep(0.05)
            progress_bar.set(i/200)
            progress_bar.update()

        progress_label.configure(text="Installed!")
        dwn_window.after(1000, self.close_progress_window(dwn_window))

        self.deiconify()
        self.artist_entry.delete(0, ctk.END)
        self.dir_entry.delete(0, ctk.END)
        self.error_label_artist.grid_forget()
        self.error_label_directory.grid_forget()
        self.focus()

    def clicked(self):
        return_or_not = False
        if not self.artist_entry.get():
            self.error_label_artist.grid(column=0, row=6,sticky ="s")
            return_or_not = True
        else:
            self.error_label_artist.grid_forget()

        if not self.dir_entry.get():
            self.error_label_directory.grid(column=0, row=7)
            return_or_not = True
        else:
            self.error_label_directory.grid_forget()

        if return_or_not:
            return
        name_of_artist = self.artist_entry.get()
        path_of_directory = self.dir_entry.get()
        self.download_window()

# Running the app
# if __name__ == "__main__":
#     app = FusicApp()
#     app.mainloop()