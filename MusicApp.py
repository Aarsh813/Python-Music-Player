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


#variables
pause_music = False
slider_used = False
filepath=r"Songs"
songs={}
w=0
a=0

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
            try: 
                pass
                #file = File(roots+'\\'+song.title())
                #image=f'images\\aw{a}.png'
                #artwork = file.tags['APIC:'].data
                #f = open(f'images\\aw{a}.png','w')
                #f.close()
                #with open(f'images\\aw{a}.png', 'wb') as img:
                #    img.write(artwork)
                #img = Image.open(f'images\\aw{a}.png')
                #img = img.resize((32,32), Image.ANTIALIAS)
                #img.save(f'images\\aw{a}.png')
                #album_cover=(f'images\\aw{a}.png')
                #tyme.sleep(0.1)
            except:
                pass
                #album_cover=('images\\unknown.png')
            a+=1
            if title == None :
                title = 'unknown'+str(w)
                w=w+1
            songs[title]=(artist,album,time,image,song.title(),t,path)

            global songs_main
            global songs_display
            songs_main = songs
            songs_display = songs

root = Tk()
root.title('MusicApp')
root.iconbitmap('images/MusicApp.ico')
root.configure(background='#000000')
root.geometry('750x400')

#song artwork
def art(song):
    file = File(songs[song][6])
    artwork = file.tags['APIC:'].data
    with open('images\image.png', 'wb') as img:
        img.write(artwork)
    img = Image.open('images\image.png')
    img = img.resize((62,62), Image.ANTIALIAS)
    img.save('images\image.png')
    
    root.one = one = tkinter.PhotoImage(file=r"images\image.png")#songs[song][7])
    #art_label = Label(player,text='',bg='#121212', fg='#03dac6',width = 60, height = 60,relief=SOLID,image=one)
    #art_label.grid(row=0,column=0)
    canvas_photo.create_image((0,0), anchor=NW, image=one) 
    canvas_photo.update()

def artwork_load(song_now):
    global two
    root.two = two = tkinter.PhotoImage(file=songs[song_now][7])
    tyme.sleep(0.1)

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
        
def dict_change():
    try:
        global songs
        songs=songs_display
    except:
        pass
    
#play function
def play(music,now):
    pygame.mixer.init()
    pygame.mixer.music.load(roots+'\\'+music)
    pygame.mixer.music.play()
    global tm
    tm = 0
    global song_now
    song_now = now #song playing now

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
    dict_change()
    art(song_now)
    played()

def played():
    dict_change()  
    try:
        current_time = tm + pygame.mixer.music.get_pos()/1000 
    except:
        current_time = pygame.mixer.music.get_pos()/1000 
    try:
        my_slider.config(value=((current_time/songs[song_now][5])*100))
    except:
        pass
    min,sec=int(current_time//60),int(current_time%60)
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

def open_path():
    subprocess.Popen('explorer "Songs"')

#get songs
def get_song(a):
    with open('images\playlist.txt','a') as r:
        r.write(str(a)+'`')

#destroy
def done():
    with open('images\playlist.txt','a') as r:
        r.write('\n')
    frame_pl2.destroy()
    
def destroy():
    #frame_edit.destroy()
    try :
        frame_edit.destroy()
    except:
        pass
    try:
        framein.destroy()
    except:
        pass

def destroy2():
    try :
        frame_pl.destroy()
    except:
        pass
    try :
        frame_pl2.destroy()
    except:
        pass
    try :
        frame_pl3.destroy()
    except:
        pass
    try :
        frame_pl4.destroy()
    except:
        pass

#selected plist
def selected(a):
    new_list={}
    a=a.split('`')
    for i in a:
        for j in songs_main :
            if i == j :
                new_list[i] = songs_main[j]
        if i == 'wdwde' :
            new_list=songs_main
    global songs_display
    songs_display=new_list
    frame_pl4.destroy()

#del selected playlist
def selected_d(a):
    with open('images\playlist.txt','r') as r:
        plists = r.readlines()
    for i in plists:
        if i.startswith(str(a.strip()))==True:
            plists.remove(i)
    with open('images\playlist.txt','w') as r:
        r.writelines(plists)
    frame_pl3.destroy()

#choose playlist
def plist_choose():
    destroy2()
    global frame_pl4
    frame_pl4 = Frame(frame2,bg='#000000', borderwidth=0,padx=10)
    frame_pl4.pack(fill=Y,side=LEFT)
    #scrollable (inside main)
    #frame-1
    framein = Frame(frame_pl4, borderwidth=0,bg='#000000', relief=SUNKEN, height=1080)
    framein.pack(fill=BOTH,expand=1)
    label=Label(framein,text='Playlist you want to choose :',padx=20,bg='#000000',fg='#fc0034',font=("Arial", 15),relief=FLAT,width=20,pady=10)
    label.pack(anchor=CENTER)
    canvas = Canvas(framein,bg='#000000')
    #scrollbar
    myscrollbar1 = Scrollbar(framein, orient="vertical", command=canvas.yview, highlightbackground='#000000')
    myscrollbar1.pack(side=RIGHT,fill=Y)
    canvas.pack(fill=BOTH,expand=1)
    #configre
    canvas.configure(yscrollcommand=myscrollbar1.set)
    canvas.bind("<Configure>",lambda x:canvas.configure(scrollregion= canvas.bbox('all')))
    canvas.bind("<Configure>",lambda y:canvas.configure(scrollregion= canvas.bbox('all')))

    frame_main = Frame(canvas,bg='#000000', borderwidth=0,padx=10)
    canvas.create_window((0,0) , window = frame_main, anchor='nw')

    a=0
    with open('images\playlist.txt','r') as r:
        plists = r.readlines()
    for i in plists:
        i=i.split(':')
        buttons=Button(frame_main,text=i[0],width=20,relief=SOLID,bg='#000000',fg='#bb86fc',font=("Arial", 15),command=partial(selected,i[1])).grid(row=a+1,column=1)
        a+=1

#delete playlist
def plist_delete():
    destroy2()
    global frame_pl3
    frame_pl3 = Frame(frame2,bg='#000000', borderwidth=0,padx=10)
    frame_pl3.pack(fill=Y,side=LEFT)
    #scrollable (inside main)
    #frame-1
    framein = Frame(frame_pl3,bg='#000000', borderwidth=0, relief=SUNKEN, height=1080)
    framein.pack(fill=BOTH,expand=1)
    label=Label(framein,text='Playlist you want to delete :',padx=20,bg='#000000',fg='#fc0034',font=("Arial", 15),relief=FLAT,width=20,pady=10)
    label.pack(anchor=CENTER)
    canvas = Canvas(framein,bg='#000000')
    #scrollbar
    myscrollbar1 = Scrollbar(framein, orient="vertical", command=canvas.yview, highlightbackground='#000000')
    myscrollbar1.pack(side=RIGHT,fill=Y)
    canvas.pack(fill=BOTH,expand=1)
    #configre
    canvas.configure(yscrollcommand=myscrollbar1.set)
    canvas.bind("<Configure>",lambda x:canvas.configure(scrollregion= canvas.bbox('all')))
    canvas.bind("<Configure>",lambda y:canvas.configure(scrollregion= canvas.bbox('all')))

    frame_main = Frame(canvas,bg='#000000', borderwidth=0,padx=10)
    canvas.create_window((0,0) , window = frame_main, anchor='nw')

    a=0
    with open('images\playlist.txt','r') as r:
        plists = r.readlines()
    for i in plists:
        i=i.split(':')
        if i[0] == 'ALL SONGS':
            pass
        else: 
            buttons=Button(frame_main,text=i[0],width=20,relief=SOLID,bg='#000000',fg='#bb86fc',font=("Arial", 15),command=partial(selected_d,i[0])).grid(row=a+1,column=1)
            a+=1

#create playlists step 2
def plist_create2():
    try:
        with open('images\playlist.txt','a') as r:
            #p=r.readlines()
            #print(p,p+[str((pname.get())+':')],[p]+[str((pname.get())+':')])
            r.write(pname.get()+':')
    except:
        pass
    destroy2()
    global frame_pl2
    frame_pl2 = Frame(frame2,bg='#000000', borderwidth=0,padx=10)
    frame_pl2.pack(fill=Y,side=LEFT)
    #scrollable (inside main)
    #frame-1
    framein = Frame(frame_pl2, borderwidth=0, relief=SUNKEN, height=1080)
    framein.pack(fill=BOTH,expand=1)
    canvas = Canvas(framein,bg='#000000')
    #scrollbar
    myscrollbar1 = Scrollbar(framein, orient="vertical", command=canvas.yview, highlightbackground='#000000')
    myscrollbar1.pack(side=RIGHT,fill=Y)
    canvas.pack(fill=BOTH,expand=1)
    #configre
    canvas.configure(yscrollcommand=myscrollbar1.set)
    canvas.bind("<Configure>",lambda x:canvas.configure(scrollregion= canvas.bbox('all')))
    canvas.bind("<Configure>",lambda y:canvas.configure(scrollregion= canvas.bbox('all')))

    frame_main = Frame(canvas,bg='#000000', borderwidth=0,padx=10)
    canvas.create_window((0,0) , window = frame_main, anchor='nw')
    a=0
    for i in songs_main:
        buttons=Button(frame_main,text=i,width=37,relief=SOLID,bg='#000000',fg='#bb86fc',command=partial(get_song,i)).grid(row=a+1,column=1)
        a+=1
    framequit = Frame(frame_pl2, borderwidth=0, relief=SUNKEN, height=1080,bg='#000000')
    framequit.pack(fill=BOTH,anchor=N)
    quit = Button(framequit,text='DONE',bg='#000000',fg='#fc0034',command=done).pack(fill=BOTH)
    root.mainloop()

#create playlists step 1
def plist_create1(): 
    destroy2()
    global frame_pl
    frame_pl = Frame(frame2,bg='#000000', borderwidth=0,padx=10)
    frame_pl.pack(fill=Y,side=LEFT)
    global blank1
    blank1 = Label(frame_pl,text='',bg='#000000', fg='#03dac6',width=10,pady=35)
    blank1.pack()
    global plabel
    plabel=Label(frame_pl,text='Name of the playlist:',padx=20,bg='#000000',fg='#fc0034',font=("Arial", 15),relief=FLAT,width=20,pady=10)
    plabel.pack(anchor=CENTER)
    global pname
    pname = Entry(frame_pl,bg='#121212',fg='#bb86fc',relief=SOLID)
    pname.pack(anchor=CENTER)
    global blank2
    blank2 = Label(frame_pl,text='',bg='#000000', fg='#03dac6',width=20,pady=10)
    blank2.pack()
    global pnext
    pnext = Button(frame_pl,text='Next',bg='#000000',fg='#bb86fc',command=plist_create2,width=10,pady=5)
    pnext.pack()

#pages
def home():
    try:
        global frame_home
        destroy()
        destroy2()
        try :
            #frame_edit.destroy()
            pass
        except:
            pass
        try:
            pass#framein.destroy()
        except:
            pass
        #scrollable (inside main)
        #frame-1
        global framein
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
        #frame-2
        frame_home = Frame(canvas,bg='#000000', borderwidth=0,padx=10)
        canvas.create_window((0,0) , window = frame_home, anchor='nw')
        #buttons
        a=0
        #albumcover=Label(frame_home,text='',width=20,pady=10,bg='#121212',fg='#23395d',relief=RAISED).grid(row=0,column=0)
        song=Label(frame_home,text='SONG NAME',width=60,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=1)
        artist=Label(frame_home,text='ARTIST',width=40,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=2)
        album=Label(frame_home,text='ALBUM',width=20,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=3)
        time=Label(frame_home,text='DURATION',width=20,pady=10,bg='#121212',fg='#fc0034',relief=RAISED).grid(row=0,column=4)
        
        global list_songs
        list_songs=[]
        for i in songs_display:
            #albumcover=Label(frame_home,width=30,height=30,pady=10,bg='#000000',fg='#bb86fc',relief=RAISED,image=two).grid(row=a+1,column=0)
            artist=Label(frame_home,text=songs[i][0],width=40,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=2)
            album=Label(frame_home,text=songs[i][1],width=20,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=3)
            time=Label(frame_home,text=songs[i][2],width=20,pady=10,bg='#000000',fg='#bb86fc',relief=SOLID).grid(row=a+1,column=4)
            buttons=Button(frame_home,text=i,width=60,pady=10,relief=SOLID,bg='#000000',fg='#bb86fc',command=partial(play,songs[i][4],i)).grid(row=a+1,column=1)
            list_songs+=[songs[i][4]]
            a+=1
    except:
        pass

def playlists():
    destroy()
    destroy2()
    try:
        options=[]
        for i in songs:
            options+=[songs[i][4]]
        #frame-2
        global frame_edit
        frame_edit = Frame(frame2,bg='#000000', borderwidth=0,padx=10,width=50,height=50,relief=SUNKEN)
        frame_edit.pack(fill=Y,side=LEFT)
        global plist_name
        create_playlist = Button(frame_edit,text='Create a new Playlist',bg='#121212', fg='#03dac6',padx=10,pady=10,command=plist_create1)
        create_playlist.grid(row=0,column=1)
        blank = Label(frame_edit,text='',bg='#000000', fg='#03dac6',width=10,pady=10)
        blank.grid(row=1,column=0)
        choose_playlist = Button(frame_edit,text='Select a Playlist',bg='#121212', fg='#03dac6',padx=10,pady=10,command=plist_choose)
        choose_playlist.grid(row=2,column=1)
        blank = Label(frame_edit,text='',bg='#000000', fg='#03dac6',width=10,pady=10)
        blank.grid(row=3,column=0)
        delete_playlist = Button(frame_edit,text='Delete a Playlist',bg='#121212', fg='#03dac6',padx=10,pady=10,command=plist_delete)
        delete_playlist.grid(row=4,column=1)

    except:
        pass

#Widgets

#bottom player
player = Frame(root,height=60,bg='#121212', borderwidth=0)
player.pack(side=BOTTOM,fill=X)
#art_label = Label(player,text='',bg='#121212', fg='#03dac6',width=10,height=3)
#art_label.grid(row=0,column=0)
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

#left menu buttons
button1 = Button(frame1, text='Home',width=10,padx=0,pady=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=home).grid(column=0,row=1)
button1 = Button(frame1, text='Playlists',width=10,padx=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=playlists).grid(column=0,row=2)
button1 = Button(frame1, text='Open Folder',width=10,padx=0,height=2,bg='#121212', fg='#03dac6',relief=FLAT,font=("Arial", 10),command=open_path).grid(column=0,row=3)

home()
root.mainloop()