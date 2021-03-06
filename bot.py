# import pyttsx3
import os
import sqlite3
import time
import sys
import random
from discord.ext import commands
from discord import File
import asyncio
from pars import *
from sw import *
from txt import opts, ansr
import threading
from analyser import *

# from COM import *

# Setup
global notes_c, cursor_n, note

notes_c = sqlite3.connect(str('notes.db'))
cursor_n = notes_c.cursor()

# engine = pyttsx3.init()

client = commands.Bot(command_prefix='/')

protocol = [[False], [0]]
global cnl, log, id_n
log = True
cnl = [[False, False]]
hello_log = []
ignor = []
text = []
global nastroi, mess_compl
nastroi = 8
mess_compl = [False, 0]
cursor_n.execute("SELECT id FROM note ORDER BY id")

lgo_img = [0,0,0,0,0,0]

min_react = 15
num_url = 3
min_budos = 1
num_img = 2

try:
    id_n = cursor_n.fetchall()[-1][0]
except:
    id_n = 0


async def Sender(msg, ch = "основной"):
    for guild in client.guilds:
        if str(guild) == "Liza":
            for channel in guild.channels:
                if str(channel) == ch:
                    await channel.send(msg)
    return

async def Sender_msg(i):
    for guild in client.guilds:
        if str(guild) == "Liza":
            for channel in guild.channels:
                if str(channel) == "картинки":
                    size = os.path.getsize(f'img/{i}')
                    if size < 8300000:
                        try:
                            await channel.send(file=File(f'img/{i}'))  # 6498888.jpeg#await channel.send(file=discord.File(f'img/{i}'))
                        except:
                            pass
                    os.remove(f'img/{i}')
    return

start_ = True
@client.event
async def on_ready():
    global start_
    if log:
        print('ok')

    if start_:
        await Sender("Я запустилась!")

    start_ = False


# await message.channel.send("Я онлайн)")


@client.event
async def on_message(message):
    global cnl
    global id_n
    global log
    global nastroi
    global note
    aut = str(message.author)

    if aut == "liza#5948":
        if log:
            print("[log] Message not used")
        return

    if cnl[0][0]:
        await message.channel.send("Тебе напоминать?")
        note = message.content.lower()
        cnl[0][1] = True
        cnl[0][0] = False
        return

    # Get command and swich commad's program
    msg = message.content.lower()

    # --------------------------------------------------------------------prl
    if msg == "отмена" and protocol[0][0]:
        await message.channel.send("Экстренный режим отключен!")
        protocol[0][0] = False
        return

    if protocol[0][0] == True:
        if msg == "1":
            await message.channel.send("ПРОТОКОЛ 1 Запущен")
            return
        if msg == "2":
            await message.channel.send("ПРОТОКОЛ 2 Запущен")
            return
        if msg == "3":
            await message.channel.send("ПРОТОКОЛ 3 Запущен")
            return
        if msg == "4":
            await message.channel.send("ПРОТОКОЛ 4 Запущен")
            return
        await message.channel.send("ПРОТОКОЛ НЕ НАЙДЕН")
        return
    # --------------------------------------------------------------------prl

    if log:
        print("[log] Message from " + aut + " : " + str(msg) + " used")

    if msg.startswith("set"):
        s = msg.split()
        if s[1] in globals():
            try:
                globals()[s[1]] = int(s[2])
            except:
                await Sender("Ошибка!")
                return
            await Sender("Переменная успешно изменена!")
            return
        else:
            await Sender("Переменная не найдена")
        return

    if msg == "help":
        pass
        return


    if msg == "log!":
        log = not log
        if log:
            await message.channel.send("Логирование включено!")
        else:
            await message.channel.send("Логирование отключено!")

    if msg == "да":
        if mess_compl[0] == True:
            cursor_n.execute(f"UPDATE note SET complete = 1 WHERE id = ?", (str(mess_compl[1])))
            notes_c.commit()
            await message.channel.send("Отметила!")
            mess_compl[0] = False
        if cnl[0][1] == True:
            cursor_n.execute(f"INSERT INTO note VALUES (?, ?, ?, ?, ?)",(id_n + 1, note, time.time(), 2 * 60 * 60 + time.time(), 0))
            notes_c.commit()
            id_n = id_n + 1
            await message.channel.send("Запомнила)")
            cnl[0][1] = False
        return

    if msg == "нет":
        if mess_compl[0] == True:
            # cursor_n.execute(f"UPDATE note SET complete = 0 WHERE id = ?", (str(mess_compl[1])))
            # notes_c.commit()
            await message.channel.send("Значит еще напомню, позже")
            mess_compl[0] = False
        if cnl[0][1] == True:
            cursor_n.execute(f"INSERT INTO note VALUES (?, ?, ?, ?, ?)",(id_n + 1, note, time.time(), 2 * 60 * 60 + time.time(), 1))
            notes_c.commit()
            id_n = id_n + 1
            await message.channel.send("Запомнила)")
            cnl[0][1] = False
        return

    if msg == "спасибо":
        await message.channel.send(str(ansr["snk"][random.randint(0, len(ansr["snk"]))]))
        return

    try:
        coman = swich(msg, opts, log=log)  # -------------------------------swich(msg)
    except:
        coman = swich(msg, opts, log=log)

    if count(aut, ignor):  # sorry()
        if coman == "sor":
            ignor.remove(aut)
            await message.channel.send(str(ansr[coman][random.randint(0, len(ansr[coman]))]))
            return
        return

    if log:
        print("[log] Comand bot: " + str(coman))

    if coman == "img":
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])

        for n in range(num_img):
            i = random.choice(check())
            await Sender_msg(i)
        num = check()
        await Sender(f'Осталось {len(num)} картинок', ch= "картинки")

    if coman == "reb":
        await  Sender("Перезапускаю react")
        client.loop.create_task(react_sender())


    if coman == "prl":
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        protocol[0][0] = True
        if log:
            print(protocol)
        return

    if coman == "dgs":
        await Sender("Запускаю диагностику! \nСтоит воздержаться от отправки сообщений до окончания проверки!")
        tas = str(asyncio.all_tasks())
        if "budos()" in tas:
            await Sender("Budos work!")
        if "react_sender()" in tas:
            await Sender("React work!")
        await Sender("Диагностика завершена")

    if coman == "nyd":  # день
        if log:
            print("NYD start")

        cursor_n.execute("SELECT * FROM note ORDER BY time")
        id_n = cursor_n.fetchall()

        for i in range(len(id_n)):
            if int(id_n[i][2]) > (time.time() - 60 * 60 * 24):
                id_nt = time.localtime(int(id_n[i][2]))

                if log:
                    print("[Log] note: " + id_n[i][1])

                await message.channel.send("Заметка от " + str(id_nt.tm_mday) + "." + str(id_nt.tm_mon) + "." + str(id_nt.tm_year) + " " + str(id_nt.tm_hour) + ":" + str(id_nt.tm_min) + " Текст: " + str(id_n[i][1]))

        await message.channel.send("Это все заметки за последние сутки")
        return

    if coman == "nyw":  # неделя
        cursor_n.execute("SELECT * FROM note ORDER BY time")
        id_n = cursor_n.fetchall()
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        for i in range(len(id_n)):
            if int(id_n[i][2]) > (time.time() - 60 * 60 * 24 * 7):
                id_nt = time.localtime(int(id_n[i][2]))

                if log:
                    print("[Log] note: " + id_n[i][1])

                await message.channel.send("Заметка от " + str(id_nt.tm_mday) + "." + str(id_nt.tm_mon) + "." + str(id_nt.tm_year) + " " + str(id_nt.tm_hour) + ":" + str(id_nt.tm_min) + " Текст: " + str(id_n[i][1]))

        await message.channel.send("Это все!")
        return

    if coman == "hello":
        f = count(aut, hello_log)
        if f > 2:
            await message.channel.send("Ты меня бесишь! Я не буду тебе отвечать пока не извинишься!")
            ignor.append(aut)
            return

        if f > 1:
            await message.channel.send("Ты что тупой? Перестань писать это!")
            hello_log.append(aut)
            return

        if str(message.author) in hello_log:
            await message.channel.send("Я уже здоровалась с тобой, меня этим не возмешь.")
            hello_log.append(aut)
            return
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        hello_log.append(aut)

        # engine.say("привет мир")
        # engine.runAndWait()
        return

    if coman == "hay":
        await message.channel.send(ansr[coman + str(int(nastroi / 2))][random.randint(0, len(ansr[coman + str(int(nastroi / 2))]))])
        return

    if coman == "hay+":
        nastroi = nastroi + 1
        if nastroi > 10:
            nastroi = 10
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        return

    if coman == "hay-":
        nastroi = nastroi - 1
        if nastroi < 0:
            nastroi = 0
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        return

    if coman == "me" or coman == "name":
        await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
        return

    if coman == "htr":
        rez = 2  # htr()  # ставить_чайник()

        if rez == 0:
            await message.channel.send("Не могу, не получается открыть COM порт(")
            return
        if rez == 1:
            await message.channel.send("COM порт открыла, но не получается отправить данные")
            return
        if rez == 2:
            await message.channel.send(
                ansr[coman][random.randint(0, len(ansr[coman]))])  # random(0,int(len(ansr["htr"])))
            return
        return

    if coman == "gdb":
        await message.channel.send("Good bye)")
        exit()

    if coman == "msc":
        await message.channel.send("Включаю музыку")
        await message.channel.send("Не забудь проапгрейдить эту функцию у меня. Я хочу знать что ты хочешь послушать, а не включать все подряд")
        # включать_музыку()
        return

    if coman == "wth":
        # получить_и_сказать погоду()
        await message.channel.send("Поидее я должна сказать погоду, но мой создатель - ленивая жопа и не прикрутил мне эту функцию")
        return

    if coman == "rfl":
        await message.channel.send("Я пока не имею чувства юмора")
        await message.channel.send("Но если меня научат смеятся то я буду смеятся над тобой)")
        return

    if coman == "ntp":
        await message.channel.send("Что нужно запомнить?")
        cnl[0][0] = True

        return

    if coman == "lht":
        rez = 2  # lht()  # свет()

        if rez == 0:
            await message.channel.send("Не могу, не получается открыть COM порт(")
            return
        if rez == 1:
            await message.channel.send("COM порт открыла, но не получается отправить данные")
            return
        if rez == 2:
            await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
            return
        return

    if coman == "lto":
        rez = 2  # lto()  # свет()

        if rez == 0:
            await message.channel.send("Не могу, не получается открыть COM порт(")
            return
        if rez == 1:
            await message.channel.send("COM порт открыла, но не получается отправить данные")
            return
        if rez == 2:
            await message.channel.send(ansr[coman][random.randint(0, len(ansr[coman]))])
            return
        return

def budos_f():
    global mess_compl, min_budos
    global text
    notes_c = sqlite3.connect(str('notes.db'))
    cursor_n = notes_c.cursor()
    cursor_n.execute("SELECT * FROM note ORDER BY time")
    id_f = cursor_n.fetchall()
    text=[]
    for i in range(len(id_f)):
        if log:
            print("[Log] Note: " + str(i) + " complete = " + str(id_f[i][4]))
        if int(id_f[i][4]) == 0:

            id_ft = time.localtime(int(id_f[i][3]))  # budos
            if log:
                print("[Log] Getting time ok")
                print(f"[Log] Note on: {id_ft.tm_hour}:{id_ft.tm_min}")
                print(f"[Log] Now: {time.localtime().tm_hour}:{time.localtime().tm_min}")

            if time.mktime(time.localtime()) > time.mktime(id_ft):
                text.append(
                    f"Заметка на {id_ft.tm_mday}.{id_ft.tm_mon}.{id_ft.tm_year}  {id_ft.tm_hour}:{id_ft.tm_min} Текст: {id_f[i][1]} \nВыполнена?")

                mess_compl[0] = True
                mess_compl[1] = int(id_f[i][0])

            if time.mktime(id_ft) - 60 * 60 * 2 < time.mktime(time.localtime()) and time.mktime(id_ft) > time.mktime(
                    time.localtime()):
                        text.append(
                    f"Заметка на {id_ft.tm_mday}.{id_ft.tm_mon}.{id_ft.tm_year}  {id_ft.tm_hour}:{id_ft.tm_min} Текст: {id_f[i][1]} \nНе забудь!")

    return

async def budos():
    global mess_compl, min_budos, text
    if log:
        print("[Log] Budos start")
    while True:

        await asyncio.sleep(60*min_budos)

        if log:
            print("[Log] New loop budos")

        threadn = threading.Thread(target=budos_f)
        threadn.start()

        while threadn.is_alive():
            await asyncio.sleep(1)

        for i in text:
            await Sender(i)




def check():
    os.chdir("img/")
    p = os.listdir()
    os.chdir("..")
    return (p)

def rdr(s):
    global num_img
    r = analys(s)
    if r==2:
        num_img = num_img - 1
        if num_img < 1:
            num_img = 1
    if r==1:
        num_img = num_img + 1
        if num_img > 10:
            num_img = 10
    return





async def react_sender():
    global num_url, min_react, num_img, lgo_img

    if log:
        print("[Log] React start")
    last_chek = len(check())
    while True:

        await asyncio.sleep(30*min_react)

        threadi = threading.Thread(target=rdr, args=[lgo_img])
        threadi.start()

        await asyncio.sleep(30 * min_react)

        if log:
            print("[Log] New loop react_sender")

        threads = threading.Thread(target=downloader, args=[log, log])
        threads.start()

        for n in range(num_img):
            i = random.choice(check())
            await Sender_msg(i)

        k = len(check())/last_chek

        lgo_img = add(lgo_img, k)

        await Sender(f'Осталось картинок: {len(check())}', ch= "картинки")
        await Sender(f'Коэфицент картинок: {k}', ch="логи")
        last_chek = len(check())





client.loop.create_task(budos())
#client.loop.run_forever(budos())
client.loop.create_task(react_sender())
#client.loop.run_forever()

token = open('token.txt', 'r').readline()
client.run(token)
