# file name : main.py
import tkinter as tk
from tkinter import messagebox
import sqlite3
import socket
import random
import tkinter.font as tkFont
from threading import Thread
from playsound import playsound


class User:
    def __init__(self, id_, nickname_):
        self.id = id_
        self.nickname = nickname_

    def getId(self):
        return self.id

    def getNickname(self):
        return self.nickname


class Pet:
    def __init__(self, name_, satiety_, species_):
        self.name = name_
        self.satiety = satiety_
        self.species = species_


def musicPlay():
    playsound('./statics/mainmusic.mp3')


music = Thread(target=musicPlay)
music.daemon = True
music.start()
# Set screen size
Height = 667
Width = 1000

# Create port numbers for networking
host = 'localhost'
port = 9998
chat_port = 9009
addr = (host, port)

connect_state = True

# background GUI
win = tk.Tk()
win.title('Cupet')
win.geometry('1000x667+100+100')
win.resizable(False, False)

# Connect to Chat Server
try:
    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.connect((host, chat_port))
except Exception as e:
    pass

# Connect to Pet Server
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(addr)
except Exception as e:
    print("Fail to connect to server")
    messagebox.showinfo(title="Error!", message="Can't connect to Server!!")
    win.destroy()  # // Interrupt

# Create Cupet database
con = sqlite3.connect("Cupet.db")
cur = con.cursor()

cur.execute(
    'CREATE TABLE IF NOT EXISTS UserInfo (id TEXT, pw TEXT ,nickname TEXT)')  # generate database with id, pw and nickname as column when cupet db does not exist
con.commit()

pet_species = ['Dog', 'Cat']  # two type of pet

# Change Pet's saying
feed_message_list = ['아이 맛있어라~!!', '많이 먹고 키 커야지!!', '너무 배불러요!']
snack_message_list = ['세상에서 제일 맛있어요!!', '너무 맛있지만 또 먹으면 살이 쪄요!', '얌얌~! 또 간식을 내놔라!']
shower_message_list = ['아이 개운해라~!!', '깨끗해진 나의 모습을 봐라~!!', '씻고나니까 더 귀여워진 것 같지!?!']
play_message_list = ['아이 재미있어라~!!', '재미있게 놀고 나니까 피곤하다!', '룰루날라~! 신나는 놀이 시간~!']

sizeUp = False  # 포만도가 10이상일 때 True 이도록 함 -> True : 몸집이 커져있는 상황을 의미


# Join membership
def join():
    if len(input_PW.get()) < 1:  # does not enter
        messagebox.showinfo(title="Error!", message="Enter a Password!")

    if input_PW.get() == input_chk_PW.get():
        print((input_ID.get(), input_PW.get(), "None"))
        cur.execute("INSERT INTO UserInfo VALUES(?, ?, ?)",
                    (input_ID.get(), input_PW.get(), "None"))  # register id and pw values in cupet.db
        print("Success Register")
        con.commit()
        loginFrame.tkraise()  # open login window
    else:
        messagebox.showinfo(title="Error!", message="Different Password!")


# Check if id is duplicated
def ID_Check():
    if len(input_ID.get()) < 4:  # id is more than 4 character
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
        messagebox.showinfo(title="Register", message="Successfully Registered!")
        loginFrame.tkraise()
    else:
        messagebox.showinfo(title="Error!", message="Different Password!")


# Open join window
def raise_join():
    input_ID.delete(0, tk.END)
    input_PW.delete(0, tk.END)
    input_chk_PW.delete(0, tk.END)
    registerFrame.tkraise()


# image by type of pet
big_pet_images = [tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png'),
                  tk.PhotoImage(file='./statics/icons2/cat/cat_basic.png')]

pet_images = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_basic.png'),
              tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png')]


# login function
def go_login():
    global user
    global sizeUp
    global pet
    cur.execute('SELECT * FROM UserInfo WHERE id=? and pw =?', (ID.get(), PW.get()))
    result = cur.fetchall()
    cur.execute('SELECT nickname FROM UserInfo WHERE id=? and pw =?', (ID.get(), PW.get()))
    nick = cur.fetchone()
    if len(result) > 0:
        messagebox.showinfo(title="Login!", message="Successfully Completed Login")
        if nick[0] == "None":
            user.id = ID.get()
            user.nickname = nick[0]
            settingFrame.tkraise()
        else:
            user.id = ID.get()
            user.nickname = nick[0]
            cur.execute('SELECT pet_name FROM PetInfo WHERE user_id=?', (user.id,))
            result = cur.fetchone()
            name_label['text'] = result[0]

            cur.execute('SELECT satiety FROM PetInfo WHERE user_id =?', (user.id,))
            pet.satiety = int(cur.fetchone()[0])
            if pet.satiety >= 10:
                sizeUp = True
            cur.execute('SELECT pet_species FROM PetInfo WHERE user_id = ?', (ID.get(),))
            spec_num = cur.fetchone()
            pet.species = int(spec_num[0])

            if sizeUp:
                pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
                pet_image_label.configure(image=big_pet_images[(spec_num[0] - 1) % 2])
            else:
                pet_image_label.configure(image=pet_images[(spec_num[0] - 1) % 2])
            mainFrame.tkraise()
    else:
        messagebox.showinfo(title="Login!", message="Failed to Login!")


species = 0


# select dog
# enter the name of the user's nickname and pet name and save it in db
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

    pet_image_label.configure(image=basic_pet_image[0])
    name_label['text'] = pet_name_entry.get()
    pet.name = pet_name_entry.get()
    pet.species = species
    pet.satiety = 0
    messagebox.showinfo(title="Completed Setting!",
                        message="Successfully set! \nPet's Name : " + pet_name_entry.get() +
                                "\nUser's Nick Name : " + user.nickname + "\nYou Selected Dog")
    mainFrame.tkraise()


# select cat
# enter the name of the user's nickname and pet name and save it in db
basic_pet_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_basic.png'),
                   tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png')]


def select_cat():
    if len(pet_name_entry.get()) < 1 or len(nickname_entry.get()) < 1:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")
        return
    global species
    species = 2

    cur.execute('UPDATE UserInfo SET nickname = ? WHERE id = ?', (nickname_entry.get(), user.id))
    user.nickname = nickname_entry.get()
    con.commit()
    pet.species = species
    pet.satiety = 0
    cur.execute(
        'CREATE TABLE IF NOT EXISTS PetInfo (user_id TEXT, pet_name TEXT, pet_species Integer, satiety Integer)')
    cur.execute('INSERT INTO PetInfo VALUES(?,?,?,?)', (user.id, pet_name_entry.get(), species, 0))
    con.commit()
    pet_image_label.configure(image=basic_pet_image[1])
    name_label['text'] = pet_name_entry.get()
    pet.name = pet_name_entry.get()

    messagebox.showinfo(title="Completed Setting!",
                        message="Successfully set! \nPet's Name : " + pet_name_entry.get() +
                                "\nUser's Nick Name : " + user.nickname + "\nYou Selected Cat")
    mainFrame.tkraise()


# communicate between pet and user
response_small_dog_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_shut.png'),
                            tk.PhotoImage(file='./statics/icons2/small_dog/sdog_shut.png'),
                            tk.PhotoImage(file='./statics/icons2/small_dog/sdogdontknow.png')]

response_big_dog_image = [tk.PhotoImage(file='./statics/icons2/dog/dog_shut.png'),
                          tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png'),
                          tk.PhotoImage(file='./statics/icons2/dog/dogdontknow.png')]

response_small_cat_image = [tk.PhotoImage(file='./statics/icons2/small_cat/scat_mouse.png'),
                            tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png'),
                            tk.PhotoImage(file='./statics/icons2/small_cat/scatdontknow.png')]

response_big_cat_image = [tk.PhotoImage(file='./statics/icons2/cat/cat_mouse.png'),
                          tk.PhotoImage(file='./statics/icons2/cat/cat_basic.png'),
                          tk.PhotoImage(file='./statics/icons2/cat/catdontknow.png')]
response_count = 1


def do_respond(message):
    global response_count
    if message.find("잘모르겠") >= 0:
        if response_count == 6:
            response_count = 1
            if sizeUp:
                if pet.species == 1:
                    img = response_big_dog_image[response_count]
                else:
                    img = response_big_cat_image[response_count]
            else:
                if pet.species == 1:
                    img = response_small_dog_image[response_count]
                else:
                    img = response_small_cat_image[response_count]
            pet_image_label.configure(image=img)
            return
        response_count += 1
        if sizeUp:
            if pet.species == 1:
                img = response_big_dog_image[(response_count % 2) + 1]
            else:
                img = response_big_cat_image[(response_count % 2) + 1]
        else:
            if pet.species == 1:
                img = response_small_dog_image[(response_count % 2) + 1]
            else:
                img = response_small_cat_image[(response_count % 2) + 1]
        pet_image_label.configure(image=img)
        mainFrame.after(300, do_respond, message)
    else:
        if response_count == 6:
            response_count = 1
            if sizeUp:
                if pet.species == 1:
                    img = response_big_dog_image[response_count]
                else:
                    img = response_big_cat_image[response_count]
            else:
                if pet.species == 1:
                    img = response_small_dog_image[response_count]
                else:
                    img = response_small_cat_image[response_count]
            pet_image_label.configure(image=img)
            return
        response_count += 1
        if sizeUp:
            if pet.species == 1:
                img = response_big_dog_image[(response_count % 2)]
            else:
                img = response_big_cat_image[(response_count % 2)]
        else:
            if pet.species == 1:
                img = response_small_dog_image[(response_count % 2)]
            else:
                img = response_small_cat_image[(response_count % 2)]
        pet_image_label.configure(image=img)
        mainFrame.after(300, do_respond, message)


def sendToServer():
    if len(input_entry.get()) > 0:
        client_socket.send(input_entry.get().encode('utf-8'))
        receive_Data = client_socket.recv(1024)
        output_label['text'] = receive_Data.decode('utf-8')
        do_respond(str(receive_Data.decode('utf-8')))
    else:
        messagebox.showinfo(title="Error!", message="Enter a value more than 1 letter!")
    input_entry.delete(0, tk.END)


# Change in image by buttons
# 샤워 이미지
dog_shower_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_shower1.png'),
                    tk.PhotoImage(file='./statics/icons2/small_dog/sdog_shower2.png'),
                    tk.PhotoImage(file='./statics/icons2/small_dog/sdog_basic.png')]

big_dog_shower_image = [tk.PhotoImage(file='./statics/icons2/dog/dog_shower1.png'),
                        tk.PhotoImage(file='./statics/icons2/dog/dog_shower2.png'),
                        tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png')]

cat_shower_image = [tk.PhotoImage(file='./statics/icons2/small_cat/scat_shower1.png'),
                    tk.PhotoImage(file='./statics/icons2/small_cat/scat_shower2.png'),
                    tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png')]

big_cat_shower_image = [tk.PhotoImage(file='./statics/icons2/cat/cat_shower1.png'),
                        tk.PhotoImage(file='./statics/icons2/cat/cat_shower2.png'),
                        tk.PhotoImage(file='./statics/icons2/cat/cat_basic.png')]

# 밥 먹기 이미지
dog_eat_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_eat1.png'),
                 tk.PhotoImage(file='./statics/icons2/small_dog/sdog_eat2.png'),
                 tk.PhotoImage(file='./statics/icons2/small_dog/sdog_basic.png')]

big_dog_eat_image = [tk.PhotoImage(file='./statics/icons2/dog/dog_eat1.png'),
                     tk.PhotoImage(file='./statics/icons2/dog/dog_eat2.png'),
                     tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png')]

cat_eat_image = [tk.PhotoImage(file='./statics/icons2/small_cat/scat_eat1.png'),
                 tk.PhotoImage(file='./statics/icons2/small_cat/scat_eat2.png'),
                 tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png')]

big_cat_eat_image = [tk.PhotoImage(file='./statics/icons2/cat/cat_eat1.png'),
                     tk.PhotoImage(file='./statics/icons2/cat/cat_eat2.png'),
                     tk.PhotoImage(file='./statics/icons2/cat/cat_basic.png')]

# 간식 먹기 이미지
dog_snack_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_snack1.png'),
                   tk.PhotoImage(file='./statics/icons2/small_dog/sdog_snack2.png'),
                   tk.PhotoImage(file='./statics/icons2/small_dog/sdog_basic.png')]

big_dog_snack_image = [tk.PhotoImage(file='./statics/icons2/dog/dog_snack1.png'),
                       tk.PhotoImage(file='./statics/icons2/dog/dog_snack2.png'),
                       tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png')]

cat_snack_image = [tk.PhotoImage(file='./statics/icons2/small_cat/scat_snack1.png'),
                   tk.PhotoImage(file='./statics/icons2/small_cat/scat_snack2.png'),
                   tk.PhotoImage(file='./statics/icons2/small_cat/scat_basic.png')]

big_cat_snack_image = [tk.PhotoImage(file='./statics/icons2/cat/cat_snack1.png'),
                       tk.PhotoImage(file='./statics/icons2/cat/cat_snack2.png'),
                       tk.PhotoImage(file='./statics/icons2/cat/cat_basic.png')]

# 놀기 이미지
dog_play_image = [tk.PhotoImage(file='./statics/icons2/small_dog/sdog_happy1.png'),
                  tk.PhotoImage(file='./statics/icons2/small_dog/sdog_shut2.png'),
                  tk.PhotoImage(file='./statics/icons2/small_dog/sdog_dirt.png')]

big_dog_play_image = [tk.PhotoImage(file='./statics/icons2/dog/dog_happy1.png'),
                      tk.PhotoImage(file='./statics/icons2/dog/dog_shut2.png'),
                      tk.PhotoImage(file='./statics/icons2/dog/dog_dirt.png')]

cat_play_image = [tk.PhotoImage(file='./statics/icons2/small_cat/scat_happy1.png'),
                  tk.PhotoImage(file='./statics/icons2/small_cat/scat_happy2.png'),
                  tk.PhotoImage(file='./statics/icons2/small_cat/scat_dirt.png')]

big_cat_play_image = [tk.PhotoImage(file='./statics/icons2/cat/cat_happy1.png'),
                      tk.PhotoImage(file='./statics/icons2/cat/cat_happy2.png'),
                      tk.PhotoImage(file='./statics/icons2/cat/cat_dirt.png')]

shower_count = 1


# enter shower button
def do_shower():
    global shower_count
    if pet.species == 1:
        if shower_count == 1:
            output_label['text'] = random.choice(shower_message_list)  # choose pet's saying after shower as a random
        if shower_count == 18:
            shower_count = 1
            if sizeUp:  # 펫의 사이즈 변화 -> 펫의 이미지 크기 변화
                img = big_dog_shower_image[shower_count + 1]
            else:
                img = dog_shower_image[shower_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL  # 모든 행동이 끝 -> 다른 버튼들을 활성화
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_dog_shower_image[shower_count % 2]
        else:
            img = dog_shower_image[shower_count % 2]
        shower_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED  # 샤워 행동이 진행 중 -> 다른 버튼들을 비활성화
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_shower)
    else:  # 고양이도 강아지와 마찬가지로 진행
        if shower_count == 1:
            output_label['text'] = random.choice(shower_message_list)
        if shower_count == 18:
            shower_count = 1
            if sizeUp:
                img = big_cat_shower_image[shower_count + 1]
            else:
                img = cat_shower_image[shower_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_cat_shower_image[shower_count % 2]
        else:
            img = cat_shower_image[shower_count % 2]
        shower_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_shower)


eat_count = 1


# enter feed button
def do_feed():
    global eat_count
    global sizeUp
    if pet.species == 1:
        if eat_count == 1:
            output_label['text'] = random.choice(feed_message_list)  # choose pet's saying after feeding as a random
        if eat_count == 18:
            eat_count = 1

            pet.satiety = pet.satiety + 2
            cur.execute('UPDATE PetInfo SET satiety = ? WHERE user_id = ?', (pet.satiety, user.id))
            con.commit()
            if pet.satiety >= 10:
                sizeUp = True
                pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')

            if sizeUp:
                img = big_dog_eat_image[eat_count + 1]
            else:
                img = dog_eat_image[eat_count + 1]

            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL  # 모든 행동이 끝 -> 다른 버튼들을 활성화
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL

            return
        if sizeUp:
            img = big_dog_eat_image[eat_count % 2]
            pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
        else:
            img = dog_eat_image[eat_count % 2]
        eat_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_feed)
    else:  # 고양이도 강아지와 마찬가지로 진행
        if eat_count == 1:
            output_label['text'] = random.choice(feed_message_list)
        if eat_count == 18:
            eat_count = 1

            pet.satiety = pet.satiety + 2
            cur.execute('UPDATE PetInfo SET satiety = ? WHERE user_id = ?', (pet.satiety, user.id))
            con.commit()
            if pet.satiety >= 10:
                sizeUp = True

            if sizeUp:
                img = big_cat_eat_image[eat_count + 1]
                pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
            else:
                img = cat_eat_image[eat_count + 1]

            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_cat_eat_image[eat_count % 2]
            pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
        else:
            img = cat_eat_image[eat_count % 2]
        eat_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_feed)


snack_count = 1


# enter snack button
def do_snack():
    global snack_count
    global sizeUp
    if pet.species == 1:
        if snack_count == 1:
            output_label['text'] = random.choice(snack_message_list)
        if snack_count == 18:
            snack_count = 1
            if sizeUp:
                img = big_dog_snack_image[snack_count + 1]
                pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
            else:
                img = dog_snack_image[snack_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL  # 모든 행동이 끝 -> 다른 버튼들을 활성화
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL
            pet.satiety = pet.satiety + 1
            cur.execute('UPDATE PetInfo SET satiety = ? WHERE user_id = ?', (pet.satiety, user.id))
            con.commit()
            if pet.satiety >= 10:
                sizeUp = True
            return
        if sizeUp:
            img = big_dog_snack_image[snack_count % 2]
            pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
        else:
            img = dog_snack_image[snack_count % 2]
        snack_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_snack)
    else:  # 고양이도 강아지와 마찬가지로 진행
        if snack_count == 1:
            output_label['text'] = random.choice(snack_message_list)
        if snack_count == 18:
            snack_count = 1

            pet.satiety = pet.satiety + 1
            cur.execute('UPDATE PetInfo SET satiety = ? WHERE user_id = ?', (pet.satiety, user.id))
            if pet.satiety >= 10:
                sizeUp = True

            if sizeUp:
                img = big_cat_snack_image[snack_count + 1]
                pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
            else:
                img = cat_snack_image[snack_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL
            snack_button['state'] = tk.NORMAL
            feed_button['state'] = tk.NORMAL
            play_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_cat_snack_image[snack_count % 2]
            pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')
        else:
            img = cat_snack_image[snack_count % 2]
        snack_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_snack)


play_count = 1


# enter play button
def do_play():
    global play_count
    if pet.species == 1:
        if play_count == 1:
            output_label['text'] = random.choice(play_message_list)
        if play_count == 18:
            play_count = 1
            if sizeUp:
                img = big_dog_play_image[play_count + 1]
            else:
                img = dog_play_image[play_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_dog_play_image[play_count % 2]
        else:
            img = dog_play_image[play_count % 2]
        play_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED

        mainFrame.after(300, do_play)
    else:  # 고양이도 강아지와 마찬가지로 진행
        if play_count == 1:
            output_label['text'] = random.choice(play_message_list)
        if play_count == 18:
            play_count = 1
            if sizeUp:
                img = big_cat_play_image[play_count + 1]
            else:
                img = cat_play_image[play_count + 1]
            pet_image_label.configure(image=img)
            shower_button['state'] = tk.NORMAL
            return
        if sizeUp:
            img = big_cat_play_image[play_count % 2]
        else:
            img = cat_play_image[play_count % 2]
        play_count += 1
        pet_image_label.configure(image=img)
        shower_button['state'] = tk.DISABLED
        play_button['state'] = tk.DISABLED
        snack_button['state'] = tk.DISABLED
        feed_button['state'] = tk.DISABLED
        mainFrame.after(300, do_play)


def back_Login():
    ID.delete(0, tk.END)
    PW.delete(0, tk.END)
    input_PW['state'] = tk.DISABLED
    input_chk_PW['state'] = tk.DISABLED
    j_join_button['state'] = tk.DISABLED
    loginFrame.tkraise()


index = 0


def rcvMsg(sock):
    global index
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            chat_space.insert(index, data.decode())
            index += 1
        except Exception as e:
            pass


def runChat():
    global sock_
    global connect_state
    msg = send_chat.get()
    send_chat.delete(0, tk.END)
    print(msg)
    if msg == '/quit':
        sock_.send(msg.encode())
        chat_space.delete(0, tk.END)
        chat_space.insert(0, '연결 종료')
        connect_state = False
    try:
        sock_.send(msg.encode())
    except Exception as e:
        chat_space.insert(0, '연결되어 있지 않습니다!')


def connectChat():
    global sock_
    if not connect_state:
        sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_.connect((host, chat_port))
    sock_.send(user.nickname.encode())
    t = Thread(target=rcvMsg, args=(sock_,))
    t.daemon = True
    t.start()


user = User("#", "#")
pet = Pet("$", 0, 0)

mes_font = tkFont.Font(family='Arial', size=15, weight='bold')  # Font of Letter

# Login Frame (로그인 창) -----------------------------------------------------

loginFrame = tk.Frame(win)
loginFrame.place(x=0, y=0)

canvas1 = tk.Canvas(loginFrame, height=Height, width=Width)
canvas1.pack()

background_image = tk.PhotoImage(file='./statics/big_login_background.png')
background_label = tk.Label(loginFrame, image=background_image)
background_label.place(relwidth=1, relheight=1)

fra1_1 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_1.place(relx=0.5, rely=0.57, relwidth=0.4, relheight=0.08, anchor='n')

text_ID = tk.Label(fra1_1, text='ID', font=mes_font)
text_ID.place(relwidth=0.25, relheight=1)

ID = tk.Entry(fra1_1, font=40)
ID.place(relx=0.3, relwidth=0.75, relheight=1)

fra1_2 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_2.place(relx=0.5, rely=0.67, relwidth=0.4, relheight=0.08, anchor='n')

text_PW = tk.Label(fra1_2, text='PWD', font=mes_font)
text_PW.place(relwidth=0.25, relheight=1)

PW = tk.Entry(fra1_2, font=40, show='*')
PW.place(relx=0.3, relwidth=0.75, relheight=1)

fra1_3 = tk.Frame(loginFrame, bg='#83e05c', bd=2)
fra1_3.place(relx=0.5, rely=0.77, relwidth=0.3, relheight=0.07, anchor='n')

join_button = tk.Button(fra1_3, text="join", font=mes_font, command=raise_join)
join_button.place(relheight=1, relwidth=0.45)

login_button = tk.Button(fra1_3, text="login", font=mes_font, command=go_login)
login_button.place(relx=0.55, relheight=1, relwidth=0.45)

# Join Frame(회원가입 창)-------------------------------------------------

registerFrame = tk.Frame(win)
registerFrame.place(x=0, y=0)
canvas2 = tk.Canvas(registerFrame, height=Height, width=Width)
canvas2.pack()

background_image2 = tk.PhotoImage(file='./statics/big_login_background.png')
background_label2 = tk.Label(registerFrame, image=background_image2)
background_label2.place(relwidth=1, relheight=1)

fra2_2 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
fra2_2.place(relx=0.5, rely=0.57, relwidth=0.6, relheight=0.07, anchor='n')

text_input_ID = tk.Label(fra2_2, text='ID', font=mes_font)
text_input_ID.place(relwidth=0.15, relheight=1)

input_ID = tk.Entry(fra2_2, font=40)
input_ID.place(relx=0.175, relwidth=0.55, relheight=1)

ID_check_button = tk.Button(fra2_2, text="check ID", font=mes_font, command=ID_Check)
ID_check_button.place(relx=0.75, relheight=1, relwidth=0.25)

back_button = tk.Button(registerFrame, text="Back", font=mes_font, relief="groove", bd=3, command=back_Login)
back_button.place(relx=0.02, rely=0.03, relheight=0.05, relwidth=0.15)

# input first PWD
j_frame2 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
j_frame2.place(relx=0.5, rely=0.67, relwidth=0.6, relheight=0.07, anchor='n')

text_input_PW = tk.Label(j_frame2, text='PWD', font=mes_font)
text_input_PW.place(relwidth=0.15, relheight=1)

input_PW = tk.Entry(j_frame2, font=40, show='*', state=tk.DISABLED)
input_PW.place(relx=0.175, relwidth=0.55, relheight=1)

j_label2_1 = tk.Label(j_frame2, bg='#83e05c')
j_label2_1.place(relx=0.75, relheight=1, relwidth=0.25)

# input second PWD to check
j_frame3 = tk.Frame(registerFrame, bg='#83e05c', bd=2)
j_frame3.place(relx=0.5, rely=0.77, relwidth=0.6, relheight=0.07, anchor='n')

text_chk_PW = tk.Label(j_frame3, text='RE-PWD', font=mes_font)
text_chk_PW.place(relwidth=0.15, relheight=1)

input_chk_PW = tk.Entry(j_frame3, font=40, state=tk.DISABLED, show='*')
input_chk_PW.place(relx=0.175, relwidth=0.55, relheight=1)

j_join_button = tk.Button(j_frame3, text="join", font=mes_font, command=register, state=tk.DISABLED)
j_join_button.place(relx=0.75, relheight=1, relwidth=0.25)

# Setting Frame (초기 설정 창)---------------------------------------------
settingFrame = tk.Frame(win)
settingFrame.place(x=0, y=0)

canvas3 = tk.Canvas(settingFrame, height=Height, width=Width)
canvas3.pack()

background_image3 = tk.PhotoImage(file='./statics/big_main_background.png')
background_label3 = tk.Label(settingFrame, image=background_image3)
background_label3.place(relwidth=1, relheight=1)

# input nick-name
nickname_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)
nickname_frame.place(relx=0.5, rely=0.2, relwidth=0.5, relheight=0.07, anchor='n')

nickname_label = tk.Label(nickname_frame, text='nickname', font=mes_font)
nickname_label.place(relwidth=0.2, relheight=1)

nickname_entry = tk.Entry(nickname_frame, font=40)
nickname_entry.place(relx=0.25, relwidth=0.75, relheight=1)

# input pet name
pet_name_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)
pet_name_frame.place(relx=0.5, rely=0.3, relwidth=0.5, relheight=0.07, anchor='n')

pet_name_label = tk.Label(pet_name_frame, text='pet name', font=mes_font)
pet_name_label.place(relwidth=0.2, relheight=1)

pet_name_entry = tk.Entry(pet_name_frame, font=40)
pet_name_entry.place(relx=0.25, relwidth=0.75, relheight=1)

# select pet
pet_select_frame = tk.Frame(settingFrame, bg='#f2f205', bd=2)
pet_select_frame.place(relx=0.5, rely=0.41, relwidth=0.4, relheight=0.07, anchor='n')

pet_select_label = tk.Label(pet_select_frame, text='펫을 선택해주세용!', bg='#ffff6b', font=mes_font)
pet_select_label.place(relwidth=1, relheight=1)

dog_select_image_frame = tk.Frame(settingFrame, bd=0, bg='#f2f205')
dog_select_image_frame.place(x=300, y=350, relwidth=0.19, relheight=0.29, anchor='n')

dog_select_image = tk.PhotoImage(file='./statics/dog.png')

dog_select_image_label = tk.Label(dog_select_image_frame, image=dog_select_image, bd=0, bg='#f2f205')
dog_select_image_label.place(x=0, y=0, relwidth=1, relheight=1)

dog_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)  # dog Frame
dog_frame.place(x=300, y=550, relwidth=0.15, relheight=0.06, anchor='n')

dog_button = tk.Button(dog_frame, text="강아지", font=mes_font, command=select_dog)
dog_button.place(relheight=1, relwidth=1)

cat_select_image_frame = tk.Frame(settingFrame, bd=0, bg='#f2f205')
cat_select_image_frame.place(x=650, y=350, relwidth=0.19, relheight=0.29, anchor='n')

cat_select_image = tk.PhotoImage(file='./statics/cat.png')

cat_select_image_label = tk.Label(cat_select_image_frame, image=cat_select_image, bd=0, bg='#f2f205')
cat_select_image_label.place(x=0, y=0, relwidth=1, relheight=1)

cat_frame = tk.Frame(settingFrame, bg='#83e05c', bd=2)  # cat Frame
cat_frame.place(x=650, y=550, relwidth=0.15, relheight=0.06, anchor='n')

cat_button = tk.Button(cat_frame, text="고양이", font=mes_font, command=select_cat)
cat_button.place(relheight=1, relwidth=1)

# sns Main Frame(메인 화면 창)-------------------------------

mainFrame = tk.Frame(win)
mainFrame.place(x=0, y=0)

canvas4 = tk.Canvas(mainFrame, height=Height, width=Width)
canvas4.pack()

background_image4 = tk.PhotoImage(file='./statics/big_main_background.png')
background_label4 = tk.Label(mainFrame, image=background_image4)

background_label4.place(relwidth=1, relheight=1)

# feed image
feed_image_frame = tk.Frame(mainFrame, bd=0)
feed_image_frame.place(x=97, y=43, relwidth=0.11, relheight=0.16, anchor='n')

feed_image = tk.PhotoImage(file='./statics/icons/basic/rice.png')

feed_image_label = tk.Label(feed_image_frame, image=feed_image, bd=0)
feed_image_label.place(x=0, y=0)

# feed button
feed_frame = tk.Frame(mainFrame, bd=0)
feed_frame.place(x=97, y=152, relwidth=0.1, relheight=0.06, anchor='n')

feed_button = tk.Button(feed_frame, text="사료", font=mes_font, bg='#f5f56e', command=do_feed)
feed_button.place(relheight=1, relwidth=1)

# snake image
snack_image_frame = tk.Frame(mainFrame, bd=0)
snack_image_frame.place(x=97, y=197, relwidth=0.11, relheight=0.16, anchor='n')

snack_image = tk.PhotoImage(file='./statics/icons/basic/snack.png')

snack_image_label = tk.Label(snack_image_frame, image=snack_image, bd=0)
snack_image_label.place(x=0, y=0)

# snake button
snack_frame = tk.Frame(mainFrame, bd=0)
snack_frame.place(x=97, y=310, relwidth=0.1, relheight=0.06, anchor='n')

snack_button = tk.Button(snack_frame, text="간식", font=mes_font, bg='#f5f56e', command=do_snack)
snack_button.place(relheight=1, relwidth=1)

# shower image
shower_image_frame = tk.Frame(mainFrame, bd=0)
shower_image_frame.place(x=97, y=347, relwidth=0.11, relheight=0.16, anchor='n')

shower_image = tk.PhotoImage(file='./statics/icons/basic/shower.png')

shower_image_label = tk.Label(shower_image_frame, image=shower_image, bd=0)
shower_image_label.place(x=0, y=0)

# shower button
shower_frame = tk.Frame(mainFrame, bd=0)
shower_frame.place(x=97, y=455, relwidth=0.1, relheight=0.06, anchor='n')

shower_button = tk.Button(shower_frame, text="샤워", font=mes_font, bg='#f5f56e', command=do_shower)
shower_button.place(relheight=1, relwidth=1)

# play image
play_image_frame = tk.Frame(mainFrame, bd=0)
play_image_frame.place(x=97, y=496, relwidth=0.11, relheight=0.16, anchor='n')

play_image = tk.PhotoImage(file='./statics/icons/basic/play.png')

play_image_label = tk.Label(play_image_frame, image=play_image, bd=0)
play_image_label.place(x=0, y=0)

# play button
play_frame = tk.Frame(mainFrame, bd=0)
play_frame.place(x=97, y=605, relwidth=0.1, relheight=0.06, anchor='n')

play_button = tk.Button(play_frame, text="놀기", font=mes_font, bg='#f5f56e', command=do_play)
play_button.place(relheight=1, relwidth=1)

# pet name
pet_name_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
pet_name_frame.place(x=495, y=170, relwidth=0.1, relheight=0.07)

name_label = tk.Label(pet_name_frame, text='이름', font=mes_font, bg='white')
name_label.place(x=0, y=0, relwidth=1, relheight=1)

# input from user
input_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
input_frame.place(x=200, y=550, relwidth=0.75, relheight=0.07)

input_entry = tk.Entry(input_frame, font=40)
input_entry.place(relwidth=0.8, relheight=1)

enter = tk.Button(input_frame, text="전송", font=mes_font, relief="solid", borderwidth=4, bg='#f5f56e',
                  command=sendToServer)
enter.place(relx=0.825, relheight=1, relwidth=0.175)

# output from pet
output_frame = tk.Frame(mainFrame, bd=2, bg='#f7f71e')
output_frame.place(relx=0.24, rely=0.12, relwidth=0.5, relheight=0.07)

output_text = '아이 신나~!'  # server로부터 받은 string으로 변경
output_label = tk.Label(output_frame, text=output_text, font=mes_font, bg='white')
output_label.place(x=0, y=0, relwidth=1, relheight=1)

# pet image
pet_image_frame = tk.Frame(mainFrame, bg='#f7f71e', bd=0)
pet_image_frame.place(x=552, y=302, relwidth=0.149, relheight=0.223, anchor='n')
# pet_image_frame.place(x=550, y=252, relwidth=0.195, relheight=0.298, anchor='n')

pet_image = tk.PhotoImage(file='./statics/icons2/dog/dog_basic.png')

pet_image_label = tk.Label(pet_image_frame, image=pet_image, bg='#f7f71e', bd=0)
pet_image_label.place(x=0, y=0)

chat_space_frame = tk.Frame(mainFrame, bg='white', bd=0)
chat_space_frame.place(x=770, y=120, relwidth=0.23, relheight=0.4)

scrollbar = tk.Scrollbar(chat_space_frame)
scrollbar.pack(side='right', fill='y')

chat_space = tk.Listbox(chat_space_frame, yscrollcommand=scrollbar.set)
chat_space.place(relx=0, rely=0.01, relheight=0.83, relwidth=0.9)

send_chat = tk.Entry(chat_space_frame, bg='yellow')
send_chat.place(relx=0, rely=0.85, relheight=0.15, relwidth=0.8)

send_button = tk.Button(chat_space_frame, text='send', bg='white', command=runChat)
send_button.place(relx=0.8, rely=0.85, relheight=0.15, relwidth=0.2)

connect_button = tk.Button(mainFrame, text='connect', relief='solid', bd=2, command=connectChat)
connect_button.place(x=770, y=385, relwidth=0.23, relheight=0.05)

disconnect_expl = tk.Label(mainFrame, bg='white', text='/quit를 입력하면 연결이 종료됩니다.')
disconnect_expl.place(x=770, y=420, relwidth=0.23, relheight=0.05)
loginFrame.tkraise()

win.mainloop()