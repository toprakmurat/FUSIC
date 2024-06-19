# import tkinter as tk
# from tkinter import ttk
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


# def turn_on():
#     entry.grid(column= 0,row = 4,pady=10)

# def turn_off():
#     entry.grid_forget()

def clicked():
    if not search_bar.get(): 
        ctk.CTkLabel(window, text="You must enter the name of artist", text_color="red").grid(column=0, row=6)
        return  

    if not entry1.get():  
        ctk.CTkLabel(window, text="You must enter the name of directory", text_color="red").grid(column=0, row=6)
        return 
    # if check_bool_var.get():
    #     name_of_track = entry.get()
    name_of_artist = search_bar.get()
    name_of_directory = entry1.get()
    new_window()

app = ctk.CTk()
app.title("App")
app.geometry("750x500")
app.resizable(False,False)
ctk.set_appearance_mode("dark")



window = ctk.CTkFrame(app,fg_color=("gray15", "gray25"),corner_radius=8)
window.pack(pady = 40,padx = 100,fill = "both",expand ="True")
window.grid_columnconfigure(0,weight=1)
for i in range(7):
    window.grid_rowconfigure(i,weight=1)

label1 = ctk.CTkLabel(window, text="Music Downloader", corner_radius=10, font=("Calibri", 35, "bold"),text_color="white")
label1.grid(row = 0,column = 0)

label2 = ctk.CTkLabel(window, text="Artist:", corner_radius=10, font=("Calibri", 20, "bold"),text_color="white")
label2.grid(row = 1,column = 0,sticky= "ws",padx = (90,0))

search_bar = ctk.CTkEntry(window, placeholder_text="Enter an artist name:", width=350, height=40)
search_bar.grid(column= 0,row = 2,pady = (0,10), padx=10)

label3 = ctk.CTkLabel(window, text="Directory:", corner_radius=10, font=("Calibri", 20, "bold"),text_color="white")
label3.grid(row = 3,column = 0,sticky= "ws",padx = (90,0))

# label1 = ctk.CTkLabel(window,text="Preferences",font= ("Times" ,25,"bold"),text_color="Black")
# label1.grid(column = 0,row = 1,sticky= "w",padx= 10,pady = 10)

# check_bool_var = ctk.BooleanVar(value = False)
# checkbox = ctk.CTkCheckBox(window, text="I want to download specific track",variable=check_bool_var,onvalue = True,offvalue=False,command= turn_on)
# checkbox.grid(column= 0,row = 2,sticky = "w",padx = 5)
# checkbox2 = ctk.CTkCheckBox(window, text="I want to download all tracks related to this artist",variable=check_bool_var,onvalue = False,offvalue=True,command= turn_off)
# checkbox2.grid(column= 0,row = 3,sticky= "w",padx =5 )

# entry = ctk.CTkEntry(window,placeholder_text="Name of the specific track:", width=350, height=40)
# entry.grid(column= 0,row = 4,pady=10)
# entry.grid_forget()

entry1 = ctk.CTkEntry(window,placeholder_text="Directory to save lyrics:", width=350, height=40)
entry1.grid(column= 0,row = 4)

button = ctk.CTkButton(window,text="Download",fg_color="darkgray",text_color="Black",command=clicked)
button.grid(column = 0,row = 5,pady=(15,0))

window.mainloop()
