from tkinter import *
import tkinter
from tinytag import TinyTag
from functools import partial
import pygame
import os
from tkinter import ttk
import eyed3
import subprocess
from mutagen import File
from PIL import ImageTk,Image 
import time as tyme

root = Tk()
root.title('MusicApp')
root.iconbitmap('images/MusicApp.ico')
root.configure(background='#000000')
root.geometry('750x400')

#variables
pause_music = False
slider_used = False
filepath=r"Songs"
songs={}
w=0

#time stamp
def timestamp(t):
    ts = tyme.time()
    ts+=t
    ts=int(ts)
    return ts

def change_time(time):
    fp = open("EasyRP-windows\config.ini",'r')
    lines = fp.readlines()
    fp.close()
    lines[26]=f'EndTimestamp={timestamp(time)}\n'
    fp = open("EasyRP-windows\config.ini",'w')
    new_lines = fp.writelines(lines)
    fp.close()

#song list
for roots, dirs, files in os.walk(filepath):
    for song in files:
        if song.endswith(".mp3"):
            audiofile = TinyTag.get(roots+'\\'+song.title(), image=True)
            t=audiofile.duration
            m=int(t//60)
            s=int(t%60)
            if s<10:
                s='0'+str(s)
            time=str(f'{m}:{s}')
            artist=(audiofile.artist)
            album=(audiofile.album)
            title=(audiofile.title)
            image=(audiofile.get_image)
            path=(roots+'\\'+song.title())
            if title == None :
                title = 'unknown'+str(w)
                w=+1
            songs[title]=(artist,album,time,image,song.title(),t,path)
        
#song artwork
def art(song):
    file = File(songs[song][6])
    artwork = file.tags['APIC:'].data
    with open('images\image.png', 'wb') as img:
        img.write(artwork)
    img = Image.open('images\image.png')
    img = img.resize((62,62), Image.ANTIALIAS)
    img.save('images\image.png')
    
    root.one = one = tkinter.PhotoImage(file=r"images\image.png")
    #art_label = Label(player,text='',bg='#121212', fg='#03dac6',width = 60, height = 60,relief=SOLID,image=one)
    #art_label.grid(row=0,column=0)
    canvas_photo.create_image((0,0), anchor=NW, image=one) 
    canvas_photo.update()

#play function
def play(music,now):
    pygame.mixer.init()
    pygame.mixer.music.load(roots+'\\'+music)
    pygame.mixer.music.play()
    global tm
    tm = 0
    global song_now
    song_now = now

    #discord not important
    ts=timestamp(songs[now][5])
    fp = open("EasyRP-windows\config.ini",'r')
    lines = fp.readlines()
    fp.close()
    lines[24]=f'Details=Listening to {now}\n'
    lines[23]=f'State=By {songs[now][0]}\n'
    lines[26]=f'EndTimestamp={ts}\n'
    fp = open("EasyRP-windows\config.ini",'w')
    new_lines = fp.writelines(lines)
    fp.close()

    try:
        if len(now) > 21:
            now=now[:21]+'...'
    except:
        pass
    song_label = Label(player,text=f'{now}', fg='#03dac6',bg='#121212',width=20,anchor='w')
    song_label.grid(row=0,column=2)
    resume = Button(player,text='pause',bg='#121212', fg='#03dac6',width=5,command=pause)
    resume.grid(row=0,column=4)
    #discord not important
    fp = open("EasyRP-windows\config.ini",'r')
    lines = fp.readlines()
    fp.close()
    lines[31]=f'SmallImage=resume\n'
    lines[32]=f'SmallImageTooltip=playing\n'
    fp = open("EasyRP-windows\config.ini",'w')
    new_lines = fp.writelines(lines)
    fp.close()
    pause_music = False 
    global music_now
    music_now = music
    time_label_2.config(text=f'{songs[song_now][2]}')
    art(song_now)
    played()

def played():
    try:
        current_time = pygame.mixer.music.get_pos()/1000 + tm
    except:
        current_time = pygame.mixer.music.get_pos()/1000 
    my_slider.config(value=((current_time/songs[song_now][5])*100)+1)
    min,sec=int(current_time//60),int(current_time%60)+1
    if sec<10:
        sec='0'+str(sec)
    time_label_1.config(text=f'{min}:{sec}')
    if pygame.mixer.music.get_busy() == False and pause_music == False:
        next()
    my_slider.after(1000,played)
    
def slide(x):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(roots+'\\'+music_now)
        pygame.mixer.music.play(start=((my_slider.get())/100)*(songs[song_now][5]))
        global slider_used
        slider_used = True
        my_slider.config(value=(my_slider.get()))
        global tm
        tm=((my_slider.get())/100)*(songs[song_now][5])
        tmd=songs[song_now][5]-tm
        change_time(tmd)
    except:
        pass

def pause():
    global pause_music
    try:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.unpause()
            resume = Button(player,text='pause',bg='#121212', fg='#03dac6',width=5,command=pause)
            resume.grid(row=0,column=4)   
            #discord not important
            fp = open("EasyRP-windows\config.ini",'r')
            lines = fp.readlines()
            fp.close()
            lines[31]=f'SmallImage=resume\n'
            lines[32]=f'SmallImageTooltip=playing\n'
            tm=((my_slider.get())/100)*(songs[song_now][5])
            tmd=songs[song_now][5]-tm
            lines[26]=f'EndTimestamp={timestamp(tmd)}\n'
            fp = open("EasyRP-windows\config.ini",'w')
            new_lines = fp.writelines(lines)
            fp.close()
            pause_music = False    
        elif pygame.mixer.music.get_busy() == True:
            try:
                pygame.mixer.music.pause()
                resume = Button(player,text='resume',bg='#121212', fg='#03dac6',width=5,command=pause)
                resume.grid(row=0,column=4)
                #discord not important
                fp = open("EasyRP-windows\config.ini",'r')
                lines = fp.readlines()
                fp.close()
                lines[31]=f'SmallImage=pause\n'
                lines[32]=f'SmallImageTooltip=paused\n'
                lines[26]=f'EndTimestamp={timestamp(0)}\n'
                fp = open("EasyRP-windows\config.ini",'w')
                new_lines = fp.writelines(lines)
                fp.close()
                pause_music = True
            except:
                pass
    except:
        pass

def next():
    try:
        a=list_songs.index(music_now)
        try:
            next_song = list_songs[a+1]
        except:
            next_song = list_songs[0]
        for i in songs:
            if next_song == songs[i][4]:
                now = i
        play(music=next_song,now=now)
    except:
        pass

def prev():
    try:
        a=list_songs.index(music_now)
        try:
            next_song = list_songs[a-1]
        except:
            next_song = list_songs[len(list_songs)]
        for i in songs:
            if next_song == songs[i][4]:
                now = i
        play(music=next_song,now=now)
    except:
        pass

def volume(x):
    try:
        pygame.mixer.music.set_volume(my_slider_vol.get())
        vol_label.config(text=int(my_slider_vol.get()*100))
    except:
        pass

def change():
    try:
        title_selected = text_title.get()
        album_selected = text_album.get()
        artist_selected = text_artist.get()
        for i in songs:
            if songs[i][4] == clicked.get():
                audiofile = songs[i][4]
                audiofile = eyed3.load(roots+'\\'+audiofile)
                audiofile.tag.artist = artist_selected
                audiofile.tag.album = album_selected
                audiofile.tag.title = title_selected
                audiofile.tag.comment = '-'
                done = Label(frame_edit,text='Successfully Saved',width=40,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID)
                done.grid(row=5,column=1)
                audiofile.tag.save()
    except:
        error = Label(frame_edit,text='Empty tags are not excepted',width=40,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID)
        error.grid(row=5,column=1)  

def open_path():
    subprocess.Popen('explorer "Songs"')

#pages
def home(canvas_home):
    try:
        global frame_home
        try :
            frame_edit.destroy()
        except:
            pass
        #frame-2
        frame_home = Frame(canvas_home,bg='#000000', borderwidth=0,padx=10)
        canvas_home.create_window((0,0) , window = frame_home, anchor='nw')
        #buttons
        a=0
        #albumcover=Label(frame,text='',width=20,pady=10,bg='#121212',fg='#23395d',relief=RAISED).grid(row=0,column=0)
        song=Label(frame_home,text='SONG NAME',width=60,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=1)
        artist=Label(frame_home,text='ARTIST',width=40,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=2)
        album=Label(frame_home,text='ALBUM',width=20,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=3)
        time=Label(frame_home,text='DURATION',width=20,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=4)
        
        global list_songs
        list_songs=[]
        for i in songs:
            #albumcover=Label(frame,image=image,width=20,pady=10,bg='#000000',fg='#bb86fc',relief=RAISED).grid(row=0,column=0)
            artist=Label(frame_home,text=songs[i][0],width=40,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=2)
            album=Label(frame_home,text=songs[i][1],width=20,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=3)
            time=Label(frame_home,text=songs[i][2],width=20,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=4)
            buttons=Button(frame_home,text=i,width=60,pady=10,relief=SOLID,bg='#000000',fg='#bb86fc',command=partial(play,songs[i][4],i)).grid(row=a+1,column=1)
            list_songs+=[songs[i][4]]
            a+=1
    except:
        pass

def edit(canvas_edit):
    try:
        try:
            frame_home.destroy()
        except:
            pass
        options=[]
        for i in songs:
            options+=[songs[i][4]]
        #frame-2
        global frame_edit
        frame_edit = Frame(canvas_edit,bg='#000000', borderwidth=0,padx=10)
        canvas_edit.create_window((0,0) , window = frame_edit, anchor='nw')
        #dropdown:
        label_edit = Label(frame_edit,text='Select Song:',width=40,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID)
        label_edit.grid(row=0,column=0)
        global clicked
        clicked = StringVar()
        clicked.set(options[0])
        drop = OptionMenu(frame_edit, clicked , *options)
        drop.grid(row=0,column=1)
        button = Button(frame_edit,text='Save changes',bg='#121212', fg='#03dac6',command=change)
        button.grid(row=5,column=0)
        tag_title = Label(frame_edit,text='Title:',pady=5,height=5,width=40,bg='#000000',fg='#bb86fc',relief=SOLID)
        tag_title.grid(row=1,column=0)
        global text_title
        text_title = Entry(frame_edit,bg='#121212',fg='#bb86fc',relief=SOLID)
        text_title.grid(row=1,column=1)
        tag_artist = Label(frame_edit,text='Artist:',pady=5,height=5,width=40,bg='#000000',fg='#bb86fc',relief=SOLID)
        tag_artist.grid(row=2,column=0)
        global text_artist
        text_artist = Entry(frame_edit,bg='#121212',fg='#bb86fc',relief=SOLID)#Text(frame_edit,pady=5,height=5,width=40,bg='#121212',fg='#bb86fc',relief=SOLID)
        text_artist.grid(row=2,column=1)
        tag_album = Label(frame_edit,text='Album:',pady=5,height=5,width=40,bg='#000000',fg='#bb86fc',relief=SOLID)
        tag_album.grid(row=3,column=0)
        global text_album
        text_album = Entry(frame_edit,bg='#121212',fg='#bb86fc',relief=SOLID)#Text(frame_edit,pady=5,height=5,width=40,bg='#121212',fg='#bb86fc',relief=SOLID)
        text_album.grid(row=3,column=1)
    except:
        pass

#Widgets

#bottom player
player = Frame(root,height=60,bg='#121212', borderwidth=0)
player.pack(side=BOTTOM,fill=X)
canvas_photo = Canvas(player, width = 60, height = 60, bg='#121212')      
canvas_photo.grid(row=0,column=0)
song_label = Label(player,text='Playing:',bg='#121212', fg='#03dac6')
song_label.grid(row=0,column=1)
#buttons
song_label = Label(player,text='',bg='#121212', fg='#03dac6',width=20,pady=20)
song_label.grid(row=0,column=2)
previous = Button(player,text='<',bg='#121212', fg='#03dac6',width=5,command=prev)
previous.grid(row=0,column=3)
resume = Button(player,text='pause',bg='#121212', fg='#03dac6',width=5,command=pause)
resume.grid(row=0,column=4)
skip = Button(player,text='>',bg='#121212', fg='#03dac6',width=5,command=next)
skip.grid(row=0,column=5)
#slider
space = Label(player,text=' ',bg='#121212', fg='#03dac6',padx=5)
space.grid(row=0,column=6)
time_label_1 = Label(player,text='0:00',bg='#121212', fg='#03dac6')
time_label_1.grid(row=0,column=7)
global my_slider
my_slider = ttk.Scale(player,from_=0,to=100,orient=HORIZONTAL,value=0,length=150,command=slide)
my_slider.grid(row=0,column=8)
time_label_2 = Label(player,text='0:00',bg='#121212', fg='#03dac6')
time_label_2.grid(row=0,column=9)
list_box = Listbox(player,bg='#121212')
#volume slider
space = Label(player,text=' ',bg='#121212', fg='#03dac6',padx=10)
space.grid(row=0,column=10)
vol_label = Label(player,text='Volume:',bg='#121212', fg='#03dac6')
vol_label.grid(row=0,column=11)
my_slider_vol = ttk.Scale(player,from_=0,to=1,orient=HORIZONTAL,value=1,length=50,command=volume)
my_slider_vol.grid(row=0,column=12)
vol_label = Label(player,text='100',bg='#121212', fg='#03dac6',width=5)
vol_label.grid(row=0,column=13)

#left menu
frame1 = Frame(root,bg='#121212', borderwidth=1, relief=SOLID,pady=10)
frame1.pack(fill=Y,side=LEFT)

#center-right main
frame2 = Frame(root,bg='#000000', borderwidth=0, relief=SOLID, height=1080)
frame2.pack(side=TOP,fill=BOTH,expand=1)#23395d
name = Label(frame2, text='MusicApp',pady=10 ,font=("Arial", 15),bg='#000000', fg='#bb86fc')
name.pack(side=TOP,fill=X)
#scrollable (inside main)
#frame-1
framein = Frame(frame2, borderwidth=0, relief=SUNKEN, height=1080)
framein.pack(fill=BOTH,expand=1)#23395d
canvas = Canvas(framein,bg='#000000')
#scrollbar
myscrollbar1 = Scrollbar(framein, orient="vertical", command=canvas.yview, highlightbackground='#000000')
myscrollbar1.pack(side=RIGHT,fill=Y)
myscrollbar2 = Scrollbar(framein, orient="horizontal", command=canvas.xview, highlightbackground='#000000')
myscrollbar2.pack(side=BOTTOM,fill=X)
canvas.pack(fill=BOTH,expand=1)
#configre
canvas.configure(yscrollcommand=myscrollbar1.set)
canvas.configure(xscrollcommand=myscrollbar2.set)
canvas.bind("<Configure>",lambda x:canvas.configure(scrollregion= canvas.bbox('all')))
canvas.bind("<Configure>",lambda y:canvas.configure(scrollregion= canvas.bbox('all')))

#left menu buttons
button1 = Button(frame1, text='Home',width=10,padx=0,pady=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=partial(home,(canvas))).grid(column=0,row=1)
button1 = Button(frame1, text='Edit Tags',width=10,padx=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=partial(edit,(canvas))).grid(column=0,row=2)
button1 = Button(frame1, text='Open Folder',width=10,padx=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=open_path).grid(column=0,row=3)

home(canvas_home=canvas)
root.mainloop()