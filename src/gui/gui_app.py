from tkinter import filedialog
import customtkinter as ctk

import time

def new_window():
    app.withdraw() 
    new_window = ctk.CTkToplevel(app)  
    new_window.title("Downloading")
    new_window.resizable(False,False)
    new_window.geometry("600x400")

    new_window._set_appearance_mode("light")

    progress_label = ctk.CTkLabel(new_window, text="Downloading...",corner_radius=8,font=("Ariel",25,"bold"))
    progress_label._set_appearance_mode("light")
    progress_label.pack(pady=60)

    progress_bar = ctk.CTkProgressBar(new_window, width=400,height=20, mode="determinate")
    progress_bar._set_appearance_mode("light")
    progress_bar.pack(pady=10)

    
    def close_progress_window():
        new_window.destroy()

    
    progress_bar.set(0)
   
    for i in range(201):
        time.sleep(0.05)
        progress_bar.set(i/200)
        progress_bar.update()
    progress_label.configure(text="Installed!")
    new_window.after(1000, close_progress_window)
    
    app.deiconify()
    search_bar.delete(0, ctk.END)
    entry1.delete(0, ctk.END)
    error_label_artist.grid_forget()  
    error_label_directory.grid_forget()
    app.focus() 

def clicked():
    if not search_bar.get(): 
        error_label_artist.grid(column=0, row=6)
        return  

    if not entry1.get():  
        error_label_directory.grid(column=0, row=6)
        return 

    name_of_artist = search_bar.get()
    path_of_directory = entry1.get()
    new_window()

def get_folder_path():
    folder_path = filedialog.askdirectory(initialdir="/", title="Select a directory")
    return folder_path

def select_and_display_path(event):
    path = get_folder_path()
    if path:
        entry1.delete(0, ctk.END)
        entry1.insert(0, path)

app = ctk.CTk()
app.title("App")
app.geometry("750x500")
app.resizable(False,False)
ctk.set_appearance_mode("dark")



window = ctk.CTkFrame(app,fg_color=("gray15", "gray25"),corner_radius=8)
window.pack(pady = 40,padx = 80,fill = "both",expand ="True")
window.grid_columnconfigure(0,weight=1)
for i in range(7):
    window.grid_rowconfigure(i,weight=1)

error_label_artist = ctk.CTkLabel(window, text="You must enter the name of artist", text_color="red")
error_label_directory = ctk.CTkLabel(window, text="You must choose where you want to upload it", text_color="red")

label1 = ctk.CTkLabel(window, text="Music Downloader", corner_radius=10, font=("Calibri", 35, "bold"),text_color="white")
label1.grid(row = 0,column = 0)

label2 = ctk.CTkLabel(window, text="Artist:", corner_radius=10, font=("Calibri", 20, "bold"),text_color="white")
label2.grid(row = 1,column = 0,sticky = "ws",padx = 83)

search_bar = ctk.CTkEntry(window, placeholder_text="Enter an artist name:", width=410, height=40)
search_bar.grid(column= 0,row = 2,pady = (0,10))

label3 = ctk.CTkLabel(window, text="Directory:", corner_radius=10, font=("Calibri", 20, "bold"),text_color="white")
label3.grid(row = 3,column = 0,sticky = "ws",padx = 83)


entry1 = ctk.CTkEntry(window,placeholder_text="Directory to save lyrics:", width=410, height=40)
entry1.grid(column= 0,row = 4)
entry1.bind("<ButtonRelease>", select_and_display_path)

# button1 = ctk.CTkButton(window,text="Select",fg_color="darkgray",text_color="Black",width=60,height=40,command =select_and_display_path)
# button1.grid(column = 1,row=4,sticky = "w")

button2 = ctk.CTkButton(window,text="Download",fg_color="darkgray",text_color="Black",command=clicked,width=160,height = 40,font=("Ariel",18))
button2.grid(column = 0,row = 5,pady=(15,0))



window.mainloop()
