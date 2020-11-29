import tkinter as tk
from tkinter import messagebox
import sqlite3
import socket


class User:
    def __init__(self,id_,nickname_):
        self.id = id_
        self.nickname = nickname_

    def getId(self):
        return self.id

    def getNickname(self):
        return self.nickname

class Pet:
    def __init__(self, name_, satiety_):
        self.name =name_
        self.satiety = satiety_

Height = 667
Width = 1000

host = 'localhost'
port = 9998
addr = (host, port)

win = tk.Tk()
win.title('Login')
win.geometry('1000x667+100+100')
win.resizable(True, True)
#Connect to server
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(addr)
except:
    print("Fail to connect to server")
    messagebox.showinfo(title="Error!", message="Can't connect to Server!!")
    win.destroy() #// Interrupt

con = sqlite3.connect("Cupet.db")
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS UserInfo (id TEXT, pw TEXT ,nickname TEXT)')
con.commit()

pet_species = ['Dog','Cat']
def join():
    if len(input_PW.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a Password!")

    if input_PW.get() == input_chk_PW.get():
        print((input_ID.get(), input_PW.get(), "None"))
        cur.execute("INSERT INTO UserInfo VALUES(?, ?, ?)", (input_ID.get(), input_PW.get(), "None"))
        print("Success Register")
        con.commit()
        # entered id and password in DB
        loginFrame.tkraise()
    else:
        messagebox.showinfo(title="Error!", message="Different Password!")


def ID_Check():
    # if it doesn't overlap
    if len(input_ID.get()) < 4:
        messagebox.showinfo(title="Error!", message="Enter a ID more than 4 letters!")
        return

    cur.execute('SELECT * FROM UserInfo WHERE id = ?', (input_ID.get(),))
    result = cur.fetchall()
    if len(result) < 1:
        print("Available ID!")
        input_PW['state'] = tk.NORMAL
        input_chk_PW['state'] = tk.NORMAL
        j_join_button['state'] = tk.NORMAL
    else:
        messagebox.showinfo(title="Error!", message="ID already exists!")
        print("Already Exists!")

def register():
    if len(input_PW.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a Password!")
        return

    if input_PW.get() == input_chk_PW.get():
        print((input_ID.get(), input_PW.get(), "None"))
        cur.execute("INSERT INTO UserInfo VALUES(?, ?, ?)", (input_ID.get(), input_PW.get(), "None"))
        print("Success Register")
        con.commit()
        # entered id and password in DB
        messagebox.showinfo(title="Register", message="Successfully Registered!")
        loginFrame.tkraise()
    else:
        messagebox.showinfo(title="Error!", message="Different Password!")

def raise_join():
    input_ID.delete(0,tk.END)
    input_PW.delete(0,tk.END)
    input_chk_PW.delete(0,tk.END)
    registerFrame.tkraise()

pet_images = [tk.PhotoImage(file='./statics/icons/dog/dog_basic.png'), tk.PhotoImage(file='./statics/icons/cat/cat_basic.png')]

def go_login():
    global user
    cur.execute('SELECT * FROM UserInfo WHERE id=? and pw =?', (ID.get(), PW.get()))
    result = cur.fetchall()
    cur.execute('SELECT nickname FROM UserInfo WHERE id=? and pw =?', (ID.get(), PW.get()))
    nick = cur.fetchone()
    if len(result) > 0:
        messagebox.showinfo(title="Login!", message="Successfully Completed Login")
        print('Login Success!')
        if nick[0] == "None":
            user.id = ID.get()
            user.nickname = nick[0]
           # label2['text'] = "ID : " + ID.get()
           # label3['text'] = "NickName :" + nick[0]
            settingFrame.tkraise()
        else:
            user.id = ID.get()
            user.nickname = nick[0]
          #  label2['text'] = "ID : " + ID.get()
          #  label3['text'] = "NickName :" + nick[0]
            cur.execute('SELECT pet_species FROM PetInfo WHERE user_id = ?',(ID.get(),))
            spec_num = cur.fetchone()
            pet_image_label.configure(image=pet_images[(spec_num[0] - 1) % 2])
            
            cur.execute('SELECT pet_name FROM PetInfo WHERE user_id=?',(user.id)
            result = cur.fetchone()
            pet_name_label['text'] = result[0]
            #h = pet_images[(spec_num[0] - 1) % 3].height()
            #w = pet_images[(spec_num[0] - 1) % 3].width()
            #pet_images[(spec_num[0] - 1) % 3] = pet_images[(spec_num[0] - 1) % 3].zoom(int(w/40),int(h/40))
            #pet.configure(image=pet_images[(spec_num[0] - 1) % 3])
            mainFrame.tkraise()

    else:
        messagebox.showinfo(title="Login!", message="Failed to Login!")

species = 0

def select_dog():
    if len(pet_name_entry.get()) < 1 or len(nickname_entry.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")
        return
    global species
    species = 1

    cur.execute('UPDATE UserInfo SET nickname = ? WHERE id = ?', (nickname_entry.get(), user.id))
    user.nickname = nickname_entry.get()
    con.commit()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS PetInfo (user_id TEXT, pet_name TEXT, pet_species Integer, satiety Integer)')
    cur.execute('INSERT INTO PetInfo VALUES(?,?,?,?)', (user.id, pet_name_entry.get(), species, 0))
    con.commit()

    messagebox.showinfo(title="Completed Setting!",
                        message="Successfully set! \nPet's Name : " + pet_name_entry.get() +
                                "\nUser's Nick Name : " + user.nickname + "\nYou Selected Dog")
    mainFrame.tkraise()


def select_cat():
    if len(pet_name_entry.get()) < 1 or len(nickname_entry.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")
        return
    global species
    species = 2

    cur.execute('UPDATE UserInfo SET nickname = ? WHERE id = ?', (nickname_entry.get(), user.id))
    user.nickname = nickname_entry.get()
    con.commit()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS PetInfo (user_id TEXT, pet_name TEXT, pet_species Integer, satiety Integer)')
    cur.execute('INSERT INTO PetInfo VALUES(?,?,?,?)', (user.id, pet_name_entry.get(), species, 0))
    con.commit()

    messagebox.showinfo(title="Completed Setting!",
                        message="Successfully set! \nPet's Name : " + pet_name_entry.get() +
                                "\nUser's Nick Name : " + user.nickname+"\nYou Selected Cat")
    mainFrame.tkraise()


def select_meerkat():
    if len(pet_name_entry.get()) < 1 or len(nickname_entry.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")
        return
    global species
    species = 3

    cur.execute('UPDATE UserInfo SET nickname = ? WHERE id = ?', (nickname_entry.get(), user.id))
    user.nickname = nickname_entry.get()
    con.commit()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS PetInfo (user_id TEXT, pet_name TEXT, pet_species Integer, satiety Integer)')
    cur.execute('INSERT INTO PetInfo VALUES(?,?,?,?)', (user.id, pet_name_entry.get(), species, 0))
    con.commit()

    messagebox.showinfo(title="Completed Setting!",
                        message="Successfully set! \nPet's Name : " + pet_name_entry.get() +
                                "\nUser's Nick Name : " + user.nickname + "\nYou Selected Meerkat")
    mainFrame.tkraise()

def sendToServer():
    if len(input_entry.get()) > 0:
        client_socket.send(input_entry.get().encode('utf-8'))
        receive_Data = client_socket.recv(1024)
        output_label['text'] = receive_Data.decode('utf-8')
        print('상대방 : ', receive_Data.decode('utf-8'))
        print("ddddd")
    else:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")

dog_shower_image = [tk.PhotoImage(file='./statics/icons/dog/dog_shower1.png'), tk.PhotoImage(file='./statics/icons/dog/dog_shower2.png'),tk.PhotoImage(file='./statics/icons/dog/dog_basic.png')]
shower_count = 1

def dog_shower():
    global shower_count
    if shower_count == 18:
        count = 1
        img = dog_shower_image[count+1]
        pet_image_label.configure(image=img)
        return
    img = dog_shower_image[shower_count % 2]
    shower_count+=1
    pet_image_label.configure(image=img)
    mainFrame.after(300,dog_shower)

dog_eat_image = [tk.PhotoImage(file='./statics/icons/dog/dog_eat1.png'), tk.PhotoImage(file='./statics/icons/dog/dog_eat2.png'),tk.PhotoImage(file='./statics/icons/dog/dog_basic.png')]
eat_count = 1
def dog_eat():
    global eat_count
    if eat_count == 18:
        eat_count = 1
        img = dog_eat_image[eat_count+1]
        pet_image_label.configure(image=img)
        return
    img = dog_eat_image[eat_count % 2]
    eat_count+=1
    pet_image_label.configure(image=img)
    mainFrame.after(300,dog_eat)

dog_snack_image = [tk.PhotoImage(file='./statics/icons/dog/dog_snack1.png'), tk.PhotoImage(file='./statics/icons/dog/dog_snack2.png'),tk.PhotoImage(file='./statics/icons/dog/dog_basic.png')]
snack_count = 1
def dog_snack():
    global snack_count
    if snack_count == 18:
        snack_count = 1
        img = dog_snack_image[snack_count+1]
        pet_image_label.configure(image=img)
        return
    img = dog_snack_image[snack_count % 2]
    snack_count+=1
    pet_image_label.configure(image=img)
    mainFrame.after(300,dog_snack)


dog_play_image = [tk.PhotoImage(file='./statics/icons/dog/dog_happy1.png'), tk.PhotoImage(file='./statics/icons/dog/dog_shut2.png'),tk.PhotoImage(file='./statics/icons/dog/dog_basic.png')]
play_count = 1
def dog_play():
    global play_count
    if play_count == 18:
        play_count = 1
        img = dog_play_image[play_count+1]
        pet_image_label.configure(image=img)
        return
    img = dog_play_image[play_count % 2]
    play_count+=1
    pet_image_label.configure(image=img)
    mainFrame.after(300,dog_play)


def back_Login():
    ID.delete(0,tk.END)
    PW.delete(0,tk.END)
    loginFrame.tkraise()

user = User("#","#")
pet = Pet("$",0)
# Login Frame (로그인 창) -----------------------------------------------------

loginFrame = tk.Frame(win)
loginFrame.place(x=0,y=0)
canvas1 = tk.Canvas(loginFrame, height=Height, width=Width)
canvas1.pack()

background_image = tk.PhotoImage(file='./statics/big_login_background.png')
background_label = tk.Label(loginFrame, image=background_image)
background_label.place(relwidth=1, relheight=1)

fra1_1 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_1.place(relx=0.5, rely=0.57, relwidth=0.4, relheight=0.08, anchor='n')

text_ID = tk.Label(fra1_1, text = 'ID')
text_ID.place(relwidth=0.25, relheight=1)

ID = tk.Entry(fra1_1, font=40)
ID.place(relx=0.3, relwidth=0.75, relheight=1)

fra1_2 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_2.place(relx=0.5, rely=0.67, relwidth=0.4, relheight=0.08, anchor='n')

text_PW = tk.Label(fra1_2, text = 'PWD')
text_PW.place(relwidth=0.25, relheight=1)

PW = tk.Entry(fra1_2, font=40,show='*')
PW.place(relx=0.3, relwidth=0.75, relheight=1)

fra1_3 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_3.place(relx=0.5, rely=0.77, relwidth=0.3, relheight=0.07, anchor='n')

join_button = tk.Button(fra1_3, text="join", font=20, command=raise_join)
join_button.place(relheight=1, relwidth=0.45)

login_button = tk.Button(fra1_3, text="login", font=20,command=go_login)
login_button.place(relx=0.55, relheight=1, relwidth=0.45)


# Join Frame(회원가입 창)-------------------------------------------------

registerFrame = tk.Frame(win)
registerFrame.place(x=0,y=0)
canvas2 = tk.Canvas(registerFrame, height=Height, width=Width)
canvas2.pack()

background_image2 = tk.PhotoImage(file='./statics/big_login_background.png')
background_label2 = tk.Label(registerFrame, image=background_image2)
background_label2.place(relwidth=1, relheight=1)

fra2_2 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
fra2_2.place(relx=0.5, rely=0.57, relwidth=0.6, relheight=0.07, anchor='n')

text_input_ID = tk.Label(fra2_2, text = 'ID')
text_input_ID.place(relwidth=0.15, relheight=1)

input_ID = tk.Entry(fra2_2, font=40)
input_ID.place(relx=0.175, relwidth=0.55, relheight=1)

ID_check_button = tk.Button(fra2_2, text="check ID", font=10,command=ID_Check)
ID_check_button.place(relx = 0.75, relheight=1, relwidth=0.25)

back_button = tk.Button(registerFrame, text="Back", font=10,relief="groove",bd=3,command=back_Login)
back_button.place(relx = 0.02,rely=0.03,relheight=0.05, relwidth=0.15)

#input first PWD
j_frame2 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
j_frame2.place(relx=0.5, rely=0.67, relwidth=0.6, relheight=0.07, anchor='n')

text_input_PW = tk.Label(j_frame2, text = 'PWD')
text_input_PW.place(relwidth=0.15, relheight=1)

input_PW = tk.Entry(j_frame2, font=40, show='*', state=tk.DISABLED)
input_PW.place(relx=0.175, relwidth=0.55, relheight=1)

j_label2_1 = tk.Label(j_frame2, bg='#83e05c')
j_label2_1.place(relx = 0.75, relheight=1, relwidth=0.25)

#input second PWD to check
j_frame3 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
j_frame3.place(relx=0.5, rely=0.77, relwidth=0.6, relheight=0.07, anchor='n')

text_chk_PW = tk.Label(j_frame3, text = 'RE-PWD')
text_chk_PW.place(relwidth=0.15, relheight=1)

input_chk_PW = tk.Entry(j_frame3, font=40, state= tk.DISABLED, show='*')
input_chk_PW.place(relx=0.175, relwidth=0.55, relheight=1)

j_join_button = tk.Button(j_frame3, text="join", font=20,command=register, state=tk.DISABLED)
j_join_button.place(relx = 0.75, relheight=1, relwidth=0.25)

# Setting Frame (초기 설정 창)---------------------------------------------
settingFrame = tk.Frame(win)
settingFrame.place(x=0,y=0)

canvas3 = tk.Canvas(settingFrame, height=Height, width=Width)
canvas3.pack()

background_image3 = tk.PhotoImage(file='./statics/big_main_background.png')
background_label3 = tk.Label(settingFrame, image=background_image3)
background_label3.place(relwidth=1, relheight=1)

#pet_select_bg = tk.PhotoImage(file='background1.png')
#pet_select_bg_lbl = tk.Label(win, image=pet_select_bg)
#pet_select_bg_lbl.place(relwidth=1, relheight=1)

#input nick-name
nickname_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)
nickname_frame.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.07, anchor='n')

nickname_label = tk.Label(nickname_frame, text = 'nickname')
nickname_label.place(relwidth=0.2, relheight=1)

nickname_entry = tk.Entry(nickname_frame, font=40)
nickname_entry.place(relx=0.25, relwidth=0.75, relheight=1)

#input pet name
pet_name_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)
pet_name_frame.place(relx=0.5, rely=0.3, relwidth=0.5, relheight=0.07, anchor='n')

pet_name_label = tk.Label(pet_name_frame, text = 'pet name')
pet_name_label.place(relwidth=0.2, relheight=1)

pet_name_entry = tk.Entry(pet_name_frame, font=40)
pet_name_entry.place(relx=0.25, relwidth=0.75, relheight=1)

#select pet
pet_select_frame = tk.Frame(settingFrame, bg='#f2f205', bd=2)
pet_select_frame.place(relx=0.5, rely=0.41, relwidth=0.4, relheight=0.07, anchor='n')

pet_select_label = tk.Label(pet_select_frame, text = '펫을 선택해주세용!', bg='#ffff6b', font=15)
pet_select_label.place(relwidth=1, relheight=1)

dog_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2) #dog Frame

dog_frame.place(x=350, y=500, relwidth=0.15, relheight=0.06, anchor='n')

dog_button = tk.Button(dog_frame, text="강아지", font=20, command=select_dog)
dog_button.place(relheight=1, relwidth=1)

cat_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)#cat Frame
cat_frame.place(x=650, y=500, relwidth=0.15, relheight=0.06, anchor='n')

cat_button = tk.Button(cat_frame, text="고양이", font=20, command=select_cat)
cat_button.place(relheight=1, relwidth=1)


#sns Main Frame(메인 화면 창)-------------------------------

mainFrame = tk.Frame(win)
mainFrame.place(x=0,y=0)
canvas4 = tk.Canvas(mainFrame, height=Height, width=Width)
canvas4.pack()

background_image4 = tk.PhotoImage(file='./statics/big_main_background.png')
background_label4 = tk.Label(mainFrame, image=background_image4)

background_label4.place(relwidth=1, relheight=1)

#feed image
feed_image_frame = tk.Frame(mainFrame, bd=0)
feed_image_frame.place(x=97, y=43, relwidth=0.11, relheight=0.16, anchor='n')

feed_image = tk.PhotoImage(file='./statics/icons/basic/rice.png')  

feed_image_label = tk.Label(feed_image_frame, image=feed_image, bd=0)
feed_image_label.place(x=0, y=0)

#feed button
feed_frame = tk.Frame(mainFrame, bd=0)
feed_frame.place(x=97, y=152, relwidth=0.1, relheight=0.06, anchor='n')

feed_button = tk.Button(feed_frame, text="사료", font=20, bg='#f5f56e',command=dog_eat)
feed_button.place(relheight=1, relwidth=1)

#snake image
snack_image_frame = tk.Frame(mainFrame, bd=0)
snack_image_frame.place(x=97, y=197, relwidth=0.11, relheight=0.16, anchor='n')

snack_image = tk.PhotoImage(file='./statics/icons/basic/snack.png')  

snack_image_label = tk.Label(snack_image_frame, image=snack_image, bd=0)
snack_image_label.place(x=0, y=0)

#snake button
snake_frame = tk.Frame(mainFrame, bd=0)
snake_frame.place(x=97, y=310, relwidth=0.1, relheight=0.06, anchor='n')

snake_button = tk.Button(snake_frame, text="간식", font=20, bg='#f5f56e', command=dog_snack)
snake_button.place(relheight=1, relwidth=1)

#shower image
shower_image_frame = tk.Frame(mainFrame, bd=0)
shower_image_frame.place(x=97, y=347, relwidth=0.11, relheight=0.16, anchor='n')

shower_image = tk.PhotoImage(file='./statics/icons/basic/shower.png')  

shower_image_label = tk.Label(shower_image_frame, image=shower_image, bd=0)
shower_image_label.place(x=0, y=0)

#shower button
shower_frame = tk.Frame(mainFrame, bd=0)
shower_frame.place(x=97, y=455, relwidth=0.1, relheight=0.06, anchor='n')

shower_button = tk.Button(shower_frame, text="샤워", font=20, bg='#f5f56e',command=dog_shower)
shower_button.place(relheight=1, relwidth=1)

#play image
play_image_frame = tk.Frame(mainFrame, bd=0)
play_image_frame.place(x=97, y=496, relwidth=0.11, relheight=0.16, anchor='n')

play_image = tk.PhotoImage(file='./statics/icons/basic/play.png')  

play_image_label = tk.Label(play_image_frame, image=play_image, bd=0)
play_image_label.place(x=0, y=0)

#play button
play_frame = tk.Frame(mainFrame, bd=0)
play_frame.place(x=97, y=605, relwidth=0.1, relheight=0.06, anchor='n')

play_button = tk.Button(play_frame, text="놀기", font=50, bg='#f5f56e',command= dog_play)
play_button.place( relheight=1, relwidth=1)

    cur.execute('SELECT pet_name FROM PetInfo WHERE user_id=?',(user.id))
    result = cur.fetchone()


#pet name
pet_name_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
pet_name_frame.place(x=455, y=170, relwidth=0.1, relheight=0.07)


name_label = tk.Label(pet_name_frame, text = '이름'. font=11, bg='white', command=go_login)
name_label.place(x=0,y=0)

#input from user
input_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
input_frame.place(x = 200, y=550, relwidth=0.75, relheight=0.07)

input_entry = tk.Entry(input_frame, font=40)
input_entry.place(relwidth=0.8, relheight=1)

enter = tk.Button(input_frame, text="전송", font=20,relief="solid",borderwidth=4,bg='#f5f56e',command=sendToServer)
enter.place(relx=0.825, relheight=1, relwidth=0.175)

#output from pet
output_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
output_frame.place(relx=0.24, rely=0.12, relwidth=0.5, relheight=0.07)

output_text = '아이 신나~!' #server로부터 받은 string으로 변경
output_label = tk.Label(output_frame, text = output_text,font=11,bg='white')
output_label.place(x=0,y=0)

#pet image
pet_image_frame = tk.Frame(mainFrame, bg='#f7f71e', bd=0)
pet_image_frame.place(x=550, y=253, relwidth=0.25, relheight=0.35, anchor='n')

pet_image = tk.PhotoImage(file='./statics/icons/dog/dog_basic.png')  

pet_image_label = tk.Label(pet_image_frame, image=pet_image, bg='#f7f71e',bd=0)
pet_image_label.place(x=0, y=0)

loginFrame.tkraise()

win.mainloop()