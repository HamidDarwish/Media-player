import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, END, Frame, Listbox, BOTH, Label
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from pygame import mixer
import os
import pygame
import time
from mutagen.mp3 import MP3
import threading
# from moviepy.editor import VideoFileClip


def show_frame(frame):
     frame.tkraise()

# colors
co1 = "#ffffff" # white
co2 = "#3C1DC6" # purple
co3 = "#333333" # blaclk

# window
root = tk.Tk()
root.title('TOP_TOP')
root.geometry('600x400+400+100')
root.configure(background=co1)
root.resizable(width=True, height=True)
root.minsize(570,180)

# logo
logo_audio1 = Image.open('audio.png')
logo_audio1 = logo_audio1.resize((140,140))
logo_audio1 = ImageTk.PhotoImage(logo_audio1)

logo_audio2 = Image.open('video.png')
logo_audio2 = logo_audio2.resize((140,140))
logo_audio2 = ImageTk.PhotoImage(logo_audio2)

logo_audio3 = Image.open('button.png')
logo_audio3 = logo_audio3.resize((140,140))
logo_audio3 = ImageTk.PhotoImage(logo_audio3)

# title logo
title_icon = PhotoImage(file='button.png')
root.iconphoto(False, title_icon)

main_frames = tk.Frame(root)
main_frames.pack(fill='both', expand=True)

main_frames.grid_rowconfigure(0, weight=1)
main_frames.grid_columnconfigure(0,weight=1)

home_page = tk.Frame(main_frames,bg='white')
video_page = tk.Frame(main_frames, bg='white')
audio_page = tk.Frame(main_frames, bg='white')
favorite_page = tk.Frame(main_frames, bg='white')

for frame in (video_page,audio_page, home_page, favorite_page):
        frame.grid(row=0, column=0, sticky='nsew')

# Create a label to use as background
# background_image = Image.open("14.jpg")
# background_photo = ImageTk.PhotoImage(background_image)
# background_label = tk.Label(home, image=background_photo)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

win = tk.Frame(root, width=600, height=30 , bg='white')
win.pack(side="bottom", fill="both")

button_logo1 = Label(audio_page,image=logo_audio1, bg='white')
button_logo1.place(x=300, y=150,anchor="center")

button_logo2 = Label(video_page,image=logo_audio2, bg='white')
button_logo2.place(x=300, y=150,anchor="center")

button_logo3 = Label(favorite_page,image=logo_audio3, bg='white')
button_logo3.place(x=300, y=150,anchor="center")

global next_song
current_position = 0
paused = False

# def audio_destroy():
#      audio_page.destroy()

# def video_destroy():
#      video_page.destroy()


def pbar_destroy():
     prog_fav.destroy()

# functions
def favorite():  
     window = tk.Tk() 
     window.title('Favorite Songs') 
     window.iconbitmap('button.png')
     window.geometry('250x300+140+100')
     window.resizable(False, False)

     Frame_fav = Frame(window, background='white')
     Frame_fav.pack(fill='both')

     Frame_bottom = Frame(window, background='lightblue', height=100)
     Frame_bottom.pack(side='bottom', fill='x')
    
     selected_folder_path = "" 
     pygame.mixer.init()

     # video_destroy()
     # Home_destroy()

     #global variables
     path = ""
     song_label=None
     duration_label = None

     # song duration
     def playtime():
          # song current length
          current_time = pygame.mixer.music.get_pos()/1000
          converted_current_time = time.strftime('%H:%M:%S',time.gmtime(current_time))
          statusbar_fav.config(text=converted_current_time)
          statusbar_fav.after(1000,playtime)

          ## song lenth

          # song = playlist.get(ACTIVE)
          # song = os.path.join(selected_folder_path, selected_song) 
          # song_mut = MP3(song)
          # song_length = song_mut.info.length
          # converted_current_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
          # statusbar.config(text=f'{converted_current_time} / {converted_current_length}')
          # statusbar.after(1000, playtime)

     def addmusic():
          global path
          path = filedialog.askdirectory()
          if path:
               os.chdir(path)
               songs = os.listdir(path)
               for song in songs:
                    if song.endswith(".mp3"):
                         playlist.insert(END, song)

     def play_music():
          global paused
          paused=False
          if paused:
               # if the music is paused, unpaused it
               pygame.mixer.music.unpause()
               paused = False
          else:
               #if the music is not paused, play the selected song
               play_selected_song()
          # call the play_time function to get song length
          playtime()

     def play_selected_song():
            global current_position, paused, selected_song
            if len(playlist.curselection())>0:
                current_index = playlist.curselection()[0]
                selected_song = playlist.get(current_index)
                full_path = os.path.join(selected_folder_path, selected_song) # add the file path again
                pygame.mixer.music.load(full_path) # load the selected song
                pygame.mixer.music.play(start=current_position)# play the song from the current position
                paused = False
                audio = MP3(full_path)
                song_duration = audio.info.length
                prog_fav["maximum"] = song_duration # set the maximum value of the pbar to the song duratio

     def next_song():
            if len(playlist.curselection())>0:
                current_index = playlist.curselection()[0]
                if current_index<playlist.size() - 1:
                    playlist.selection_clear(0,tk.END)
                    playlist.selection_set(current_index+1)
                    play_selected_song()   

     def previous_song():
        if len(playlist.curselection())>0:
            current_index = playlist.curselection()[0]
            if current_index>0:
                playlist.selection_clear(0, tk.END)
                playlist.selection_set(current_index - 1)
                play_selected_song()

     def skip_song_backward():
          if not pygame.mixer.get_init():
               pygame.mixer.init()

          pygame.mixer.music.load(selected_song)
          pygame.mixer.music.play()
          current_pos = pygame.mixer.music.get_pos()/1000
          new_pos = max(0, current_pos-10)
          pygame.mixer.music.set_pos(new_pos)

     def skip_song_forward(seconds=10):
          if pygame.mixer.music.get_busy():
               current_pos = pygame.mixer.music.get_pos()/1000
               new_pos = current_pos+seconds
               pygame.mixer.music.play(start=new_pos)

     def update_progress():
          global current_position
          while True:
               if pygame.mixer.music.get_busy() and not paused:
                    current_position = pygame.mixer.music.get_pos() / 1000
                    prog_fav["value"] = current_position

                    # check if the currnt song has reached its maximum duration
                    if current_position >= prog_fav["maximum"]:
                         pause_music() # stop the music playback
                         prog_fav["value"] = 0 # reset the pbar

                    root.update()
               time.sleep(0.1)
          
     def pause_music():
          global paused
          # pause the currently playing music
          pygame.mixer.music.pause()
          paused = True

     def delete():
         playlist.delete(ANCHOR)
         my_label.config(text='')

     def delete_all():
        playlist.delete(0,END) 
        
     def top():
              window.destroy()

     # initialize pygame mixer
     pygame.mixer.init()

     scroll = Scrollbar(Frame_fav, orient='vertical')
     playlist = Listbox(Frame_fav, width=100, font=("Times new roman", 10), bg='lightblue', fg='grey', selectbackground='lightblue', cursor = 'hand2', yscrollcommand=scroll.set)
     scroll.config(command=playlist.yview)
     scroll.pack(side='right', fill='y')
     playlist.pack(side=RIGHT, fill=BOTH)

     # # create a thread to update the progress bar
     pt = threading.Thread(target=update_progress)
     pt.daemon = True
     pt.start()

     # icons as buttons
     icon_0 = Image.open('stop.ico')
     icon_0 = icon_0.resize((25,25))
     icon_0 = ImageTk.PhotoImage(icon_0)
     pause_button = tk.Button(win,image=icon_0,bg='white',bd=0, command=pause_music)
     pause_button.place(relx=0.53, y=0, relwidth=0.060)

     icon1 = Image.open('play.png')
     icon1 = icon1.resize((25,25))
     icon1 = ImageTk.PhotoImage(icon1)
     play_button = tk.Button(win,bg='white', bd=0,image=icon1,command=play_music)
     play_button.place(relx=0.47, y=0, relwidth=0.060)

     icon2 = Image.open('next-track.png')
     icon2 = icon2.resize((25,25))
     icon2 = ImageTk.PhotoImage(icon2)
     next_button = tk.Button(win,image=icon2,bg='white',bd=0,command=next_song)
     next_button.place(relx=0.59, y=0, relwidth=0.060)

     icon3 = Image.open('previous-track.png')
     icon3 = icon3.resize((25,25))
     icon3 = ImageTk.PhotoImage(icon3)
     previous_button = tk.Button(win,bd=0,bg='white',image=icon3, command=previous_song)
     previous_button.place(relx=0.41, rely=0, relwidth=0.060)
     
     icon4 = Image.open('skip_10_sec.png')
     icon4 = icon4.resize((25,25))
     icon4 = ImageTk.PhotoImage(icon4)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white',image=icon4, command=skip_song_forward)
     skip_10_sec_button.place(relx=0.35, rely=0, relwidth=0.060)

     icon5 = Image.open('skip_10_sec.png')
     icon5 = icon5.resize((25,25))
     icon5 = ImageTk.PhotoImage(icon5)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white', image=icon5,command=skip_song_backward)
     skip_10_sec_button.place(relx=0.65, rely=0, relwidth=0.060)

    # label and buttons
     my_label = Label(root, text='')
     my_label.pack(pady=5)
    
     b = Button(Frame_bottom, text='Delete All',font=("calibri", 8),width=8,height=1, bd=0, bg='white',command=delete_all)
     b.place(x=18, y=17)
    
     b1 = Button(Frame_bottom, text='Delete',font=("calibri", 8),width=7,height=1, bd=0, bg='white', command=delete)
     b1.place(x=75, y=17)

     b2 = Button(Frame_bottom, text='Add song', font=("calibri", 8),width=8,height=1, bd=0, bg='white', fg='black', command=addmusic)
     b2.place(x=177, y=17)

     b3 = Button(Frame_bottom, text='Close', font=("calibri", 8),width=7,height=1, bd=0, bg='white', fg='black', command=top)
     b3.place(x=126, y=17)

     bottom_label  = Label(Frame_bottom, text='Select Your Favorite Folder',font=("calibri", 12, ''))
     bottom_label.place(x=35, y=55)

     scroll.config(command=playlist.yview)
     scroll.pack(side='right')
   
     playlist.pack(pady=10)

     my_menu = Menu(root)
     root.config(menu=my_menu)

    # add song Menu
     add_song_menu = Menu(my_menu)
     my_menu.add_cascade(menu=add_song_menu)
     add_song_menu.add_command(command=addmusic)

     window.mainloop()
def addplay():
     root = tk.Tk()
     root.title('Audio')
     root.geometry('250x300+140+100')
     root.iconbitmap('button.png')
     root.resizable(width=False, height=False)

     Frame_Music = Frame(root, background='white')
     Frame_Music.place(width=250, height=250)
    
     selected_folder_path = "" 
     pygame.mixer.init()

     #global variables
     path = ""
     song_label=None
     duration_label = None
     
     def initialize_pygame():
          pygame.mixer.init()
     # song duration
     def playtime():
          current_time = pygame.mixer.music.get_pos()/1000
          converted_current_time = time.strftime('%H:%M:%S',time.gmtime(current_time))
         # statusbar.config(text=int(current_time))
          statusbar_audio.config(text=converted_current_time)
          statusbar_audio.after(1000,playtime)
          
          # song = playlist.get(ACTIVE)
          # song = os.path.join(selected_folder_path, selected_song) 
          # song_mut = MP3(song)
          # song_length = song_mut.info.length
          # converted_current_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
          # statusbar.config(text=f'{converted_current_time} / {converted_current_length}')
          # statusbar.after(1000, playtime)


     def addmusic():
          global path
          path = filedialog.askdirectory()
          if path:
               os.chdir(path)
               songs = os.listdir(path)
               for song in songs:
                    if song.endswith(".mp3"):
                         playlist.insert(END, song)

     def play_music():
          global paused
          paused=False
          if paused:
               # if the music is paused, unpaused it
               pygame.mixer.music.unpause()
               paused = False
          else:
               #if the music is not paused, play the selected song
               play_selected_song()
          # call the play_time function to get song length
          playtime()

     def play_selected_song():
            global current_position, paused, selected_song
            if len(playlist.curselection())>0:
                current_index = playlist.curselection()[0]
                selected_song = playlist.get(current_index)
                full_path = os.path.join(selected_folder_path, selected_song) # add the file path again
                pygame.mixer.music.load(full_path) # load the selected song
                pygame.mixer.music.play(start=current_position)# play the song from the current position
                paused = False
                audio = MP3(full_path)
                song_duration = audio.info.length
                prog_audio["maximum"] = song_duration # set the maximum value of the pbar to the song duratio

     def next_song():
            if len(playlist.curselection())>0:
                current_index = playlist.curselection()[0]
                if current_index<playlist.size() - 1:
                    playlist.selection_clear(0,tk.END)
                    playlist.selection_set(current_index+1)
                    play_selected_song()    
     def previous_song():
        if len(playlist.curselection())>0:
            current_index = playlist.curselection()[0]
            if current_index>0:
                playlist.selection_clear(0, tk.END)
                playlist.selection_set(current_index - 1)
                play_selected_song()

     def skip_song_backward():
          if not pygame.mixer.get_init():
               pygame.mixer.init()

          pygame.mixer.music.load(selected_song)
          pygame.mixer.music.play()
          current_pos = pygame.mixer.music.get_pos()/1000
          new_pos = max(0, current_pos-10)
          pygame.mixer.music.set_pos(new_pos)

     def skip_song_forward(seconds=10):
          if pygame.mixer.music.get_busy():
               current_pos = pygame.mixer.music.get_pos()/1000
               new_pos = current_pos+seconds
               pygame.mixer.music.play(start=new_pos)

     def update_progress():
          global current_position
          while True:
               if pygame.mixer.music.get_busy() and not paused:
                    current_position = pygame.mixer.music.get_pos() / 1000
                    prog_audio["value"] = current_position

                    # check if the currnt song has reached its maximum duration
                    if current_position >= prog_audio["maximum"]:
                         pause_music() # stop the music playback
                         prog_audio["value"] = 0 # reset the pbar

                    root.update()
               time.sleep(0.1)
          
     def pause_music():
          global paused
          # pause the currently playing music
          pygame.mixer.music.pause()
          paused = True

     
     # initialize pygame mixer
     pygame.mixer.init()

     scroll = Scrollbar(Frame_Music, orient='vertical')
     playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg='lightblue', fg='grey', selectbackground='lightblue', cursor = 'hand2', yscrollcommand=scroll.set)
     scroll.config(command=playlist.yview)
     scroll.pack(side='right', fill='y')
     playlist.pack(side=RIGHT, fill=BOTH)

     # # create a thread to update the progress bar
     pt = threading.Thread(target=update_progress)
     pt.daemon = True
     pt.start()

     # icons
     icon_0 = Image.open('stop.ico')
     icon_0 = icon_0.resize((25,25))
     icon_0 = ImageTk.PhotoImage(icon_0)
     pause_button = tk.Button(win,image=icon_0,bg='white',bd=0, command=pause_music)
     pause_button.place(relx=0.53, y=0, relwidth=0.060)

     icon1 = Image.open('play.png')
     icon1 = icon1.resize((25,25))
     icon1 = ImageTk.PhotoImage(icon1)
     play_button = tk.Button(win,bg='white', bd=0,image=icon1,command=play_music)
     play_button.place(relx=0.47, y=0, relwidth=0.060)

     icon2 = Image.open('next-track.png')
     icon2 = icon2.resize((25,25))
     icon2 = ImageTk.PhotoImage(icon2)
     next_button = tk.Button(win,image=icon2,bg='white',bd=0,command=next_song)
     next_button.place(relx=0.59, y=0, relwidth=0.060)

     icon3 = Image.open('previous-track.png')
     icon3 = icon3.resize((25,25))
     icon3 = ImageTk.PhotoImage(icon3)
     previous_button = tk.Button(win,bd=0,bg='white',image=icon3, command=previous_song)
     previous_button.place(relx=0.41, rely=0, relwidth=0.060)
     
     icon4 = Image.open('skip_10_sec.png')
     icon4 = icon4.resize((25,25))
     icon4 = ImageTk.PhotoImage(icon4)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white',image=icon4, command=skip_song_backward)
     skip_10_sec_button.place(relx=0.35, rely=0, relwidth=0.060)

     icon5 = Image.open('skip_10_sec.png')
     icon5 = icon5.resize((25,25))
     icon5 = ImageTk.PhotoImage(icon5)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white', image=icon5, command=lambda:skip_song_forward(10))
     skip_10_sec_button.place(relx=0.65, rely=0, relwidth=0.060)

     def top():
          root.destroy()

     #create a progress bar to indicate the current song`s progress
     # pbar = Progressbar(audio_page, length=450, mode="determinate")
     # pbar.place(relx=0.23, rely=0.920, relwidth=0.75)

     # button 2
     bstop = tk.Button(root, text='Close', font=("Times new roman", 10),bd=0, bg='lightblue', command=top)
     bstop.place(x=65, y=270)

     but = tk.Button(root, text='Select Folder', bd=0, background='lightblue', command=addmusic)
     but.place(x=110, y=270)

     # statusbar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
     # statusbar.pack(fill='x', side='bottom')
     # song_label = ttk.Label(root, text="Current song: None")
     # song_label.pack(pady=10)

     # duration_label = ttk.Label(root, text='Duration: 00:00')
     # duration_label.pack(pady=10)

     initialize_pygame()
     root.mainloop()

# Initialize pygame mixer
pygame.mixer.init()

# Global variables
selected_folder_path = ""
playlist = None
player = None
playing = False
paused = False
current_video_index = 0

def video_play():
     global playlist
     window = tk.Tk()
     window.title('Video')
     window.geometry('250x300+140+100')
     window.iconbitmap('button.png')
     window.resizable(width=False, height=False)
     
     Frame_video = Frame(window, background='white')
     Frame_video.place(width=250, height=250)

     def add_videos_to_playlist():
          global selected_folder_path, playlist
          selected_folder_path = filedialog.askdirectory()
          if selected_folder_path:
               os.chdir(selected_folder_path)
               videos = [video for video in os.listdir(selected_folder_path) if video.endswith(".mp4")]
               playlist.delete(0, END)
               for video in videos:
                    playlist.insert(END, video)

     def play_selected_video():
          global player, playing, current_video_index
          stop_video()
          if playlist.curselection():
               current_video_index = playlist.curselection()[0]
               selected_video = playlist.get(current_video_index)
               video_path = os.path.join(selected_folder_path, selected_video)
               play_video(video_path)

     def play_video(video_path, sound=True):
          global player, playing
          stop_video()
          def play_video_thread():
               global player, playing
               playing = True
               player = VideoFileClip(video_path)
               player.preview(fps=30, audio=sound)
               playing = False

          play_thread = threading.Thread(target=play_video_thread)
          play_thread.start()

     def stop_video():
          global player, playing
          if player is not None:
               player.close()
               playing = False

     def pause_video():
          global paused
          if pygame.mixer.music.get_busy():
               if paused:
                    pygame.mixer.music.unpause()
                    paused = False
               else:
                    pygame.mixer.music.pause()
                    paused = True

     def play_next_video():
          global current_video_index
          if current_video_index < playlist.size() - 1:
               current_video_index += 1
               selected_video = playlist.get(current_video_index)
               video_path = os.path.join(selected_folder_path, selected_video)
               play_video(video_path)

     def play_previous_video():
          global current_video_index
          if current_video_index > 0:
               current_video_index -= 1
               selected_video = playlist.get(current_video_index)
               video_path = os.path.join(selected_folder_path, selected_video)
               play_video(video_path)

     def skip_forward():
          global player
          if player is not None:
               current_time = player.get(0) + 10
               player.set(0, current_time)

     def skip_backward():
          global player
          if player is not None:
               current_time = max(0, player.get(0) - 10)
               player.set(0, current_time)
               
     def top():
          window.destroy()

     # Create playlist
     playlist = Listbox(Frame_video, width=30, font=("Times new roman", 10), bg='lightblue', fg='grey', selectbackground='lightblue', cursor='hand2')
     playlist.pack(side=tk.LEFT, fill=BOTH, expand=True)

     # Scrollbar for playlist
     scrollbar = ttk.Scrollbar(Frame_video, orient=tk.VERTICAL, command=playlist.yview)
     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
     playlist.config(yscrollcommand=scrollbar.set)


     b_add_video = tk.Button(window, text='Close', font=("Times new roman", 10),bd=0, bg='lightblue', command=top)
     b_add_video.place(x=65, y=270)

     but_select = tk.Button(window, text='Select Folder', bd=0, background='lightblue', command=add_videos_to_playlist)
     but_select.place(x=110, y=270)
  
     # icons as buttons
     icon_0 = Image.open('stop.ico')
     icon_0 = icon_0.resize((25,25))
     icon_0 = ImageTk.PhotoImage(icon_0)
     next_button = tk.Button(win,image=icon_0,bd=0,bg='white', command=stop_video)
     next_button.place(relx=0.53, y=0, relwidth=0.060)

     icon1 = Image.open('play.png')
     icon1 = icon1.resize((25,25))
     icon1 = ImageTk.PhotoImage(icon1)
     next_button = tk.Button(win, bd=0,bg='white',image=icon1, command=play_selected_video)
     next_button.place(relx=0.47, y=0, relwidth=0.060)

     icon2 = Image.open('next-track.png')
     icon2 = icon2.resize((25,25))
     icon2 = ImageTk.PhotoImage(icon2)
     next_button = tk.Button(win,image=icon2,bg='white',bd=0, command=play_next_video)
     next_button.place(relx=0.59, y=0, relwidth=0.060)

     icon3 = Image.open('previous-track.png')
     icon3 = icon3.resize((25,25))
     icon3 = ImageTk.PhotoImage(icon3)
     previous_button = tk.Button(win,bd=0,bg='white',image=icon3, command=play_previous_video)
     previous_button.place(relx=0.41, rely=0, relwidth=0.060)

     icon4 = Image.open('skip_10_sec.png')
     icon4 = icon4.resize((25,25))
     icon4 = ImageTk.PhotoImage(icon4)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white',image=icon4, command=skip_forward)
     skip_10_sec_button.place(relx=0.35, rely=0, relwidth=0.060)

     icon5 = Image.open('skip_10_sec.png')
     icon5 = icon5.resize((25,25))
     icon5 = ImageTk.PhotoImage(icon5)
     skip_10_sec_button = tk.Button(win,bd=0,bg='white', image=icon5, command=skip_backward)
     skip_10_sec_button.place(relx=0.65, rely=0, relwidth=0.060)


     

     
     # Run the Tkinter main loop
     window.mainloop()

# volume control
def volume():
     scale = ttk.Scale(home_page, orient='vertical')
     scale.pack()
def volume(vol):
     volume = int(vol)/100
     mixer.music.set_volume(volume)
     pygame.mixer.init()
def volume_bar():
     global scale
     scale = Scale(root, from_=0, to=100, orient=VERTICAL, bg='white', length=100, width=15, command=volume)
     scale.place(x=550, y=260)

     scale.set(30)

paused = False
# pause and unpause the song
def pause_file():
     pygame.mixer.music.pause()

is_playing=False

#logo
icon0 = Image.open('button.png')
icon0 = icon0.resize((130,130))
icon0 = ImageTk.PhotoImage(icon0)
button_icon = Label(home_page,image=icon0, bg='white')
button_icon.place(x=300, y=150,anchor="center")
button_icon.pack(expand=True)

# icons as buttons
icon_0 = Image.open('stop.ico')
icon_0 = icon_0.resize((25,25))
icon_0 = ImageTk.PhotoImage(icon_0)
next_button = tk.Button(win,image=icon_0,bd=0,bg='white')
next_button.place(relx=0.53, y=0, relwidth=0.060)

icon1 = Image.open('play.png')
icon1 = icon1.resize((25,25))
icon1 = ImageTk.PhotoImage(icon1)
next_button = tk.Button(win, bd=0,bg='white',image=icon1)
next_button.place(relx=0.47, y=0, relwidth=0.060)

icon2 = Image.open('next-track.png')
icon2 = icon2.resize((25,25))
icon2 = ImageTk.PhotoImage(icon2)
next_button = tk.Button(win,image=icon2,bg='white',bd=0)
next_button.place(relx=0.59, y=0, relwidth=0.060)

icon3 = Image.open('previous-track.png')
icon3 = icon3.resize((25,25))
icon3 = ImageTk.PhotoImage(icon3)
previous_button = tk.Button(win,bd=0,bg='white',image=icon3)
previous_button.place(relx=0.41, rely=0, relwidth=0.060)

icon4 = Image.open('skip_10_sec.png')
icon4 = icon4.resize((25,25))
icon4 = ImageTk.PhotoImage(icon4)
skip_10_sec_button = tk.Button(win,bd=0,bg='white',image=icon4)
skip_10_sec_button.place(relx=0.35, rely=0, relwidth=0.060)

icon5 = Image.open('skip_10_sec.png')
icon5 = icon5.resize((25,25))
icon5 = ImageTk.PhotoImage(icon5)
skip_10_sec_button = tk.Button(win,bd=0,bg='white', image=icon5)
skip_10_sec_button.place(relx=0.65, rely=0, relwidth=0.060)

icon8 = Image.open('sound.png')
icon8 = icon8.resize((25,25))
icon8 = ImageTk.PhotoImage(icon8)
sound_button = tk.Button(win,bd=0,bg='white',image=icon8, command=lambda:volume_bar())
sound_button.place(relx=0.94, rely=0, relwidth=0.060)

icon9 = Image.open('video.png')
icon9 = icon9.resize((25,25))
icon9 = ImageTk.PhotoImage(icon9)
video_button = tk.Button(win,bd=0,bg='white',image=icon9, command=lambda:(show_frame(video_page), video_play()))
video_button.place(relx=0.060, rely=0, relwidth=0.060)

icon10 = Image.open('audio.png')
icon10 = icon10.resize((25,25))
icon10 = ImageTk.PhotoImage(icon10)
audio_button = tk.Button(win,bd=0,bg='white',image=icon10, command=lambda:(show_frame(audio_page), addplay(), pbar_destroy()))
audio_button.place(relx=0.12, rely=0, relwidth=0.060)

icon11 = Image.open('heart.png')
icon11 = icon11.resize((25,25))
icon11 = ImageTk.PhotoImage(icon11)
heart_button = tk.Button(win,bd=0,bg='white',image=icon11, command=lambda:(show_frame(favorite_page), favorite()))
heart_button.place(relx=0.18, rely=0, relwidth=0.060)

icon12 = Image.open('menu.png')
icon12 = icon12.resize((25,25))
icon12 = ImageTk.PhotoImage(icon12)
home_button = tk.Button(win,bd=0,bg='white',image=icon12, command=lambda:(show_frame(home_page)))
home_button.place(relx=0, rely=0, relwidth=0.060)

statusbar_audio = Label(audio_page, text='00:00:00 / 00:00:00', bg='white', fg='black')
statusbar_audio.place(relx=0.017, rely=0.920, relwidth=0.2)

statusbar_video = Label(video_page, text='00:00:00 / 00:00:00', bg='white', fg='black')
statusbar_video.place(relx=0.017, rely=0.920, relwidth=0.2)

statusbar_fav = Label(favorite_page, text='00:00:00 / 00:00:00', font=('Helvetica', 10), bg='white', fg='black')
statusbar_fav.place(relx=0.017, rely=0.920, relwidth=0.2)

prog_video = Progressbar(video_page, length=450, mode="determinate")
prog_video.place(relx=0.23, rely=0.920, relwidth=0.75)

prog_audio= Progressbar(audio_page, length=450, mode="determinate")
prog_audio.place(relx=0.23, rely=0.920, relwidth=0.75)

prog_fav= Progressbar(favorite_page, length=450, mode="determinate")
prog_fav.place(relx=0.23, rely=0.920, relwidth=0.75)

show_frame(home_page)

root.mainloop()