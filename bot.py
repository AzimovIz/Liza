#import pyttsx3
import sqlite3
import time
import random
import discord
from discord.ext import commands
import asyncio

from sw import *
from txt import opts, ansr
#from COM import *

#Setup
global notes_c, cursor_n
notes_c = sqlite3.connect(str('notes.db'))
cursor_n = notes_c.cursor()

#engine = pyttsx3.init()

client = commands.Bot(command_prefix = '/')

protocol=[[False],[0]]
global cnl, log, id_n
log = True
cnl = [[False, False]]
hello_log = []
ignor = []
global nastroi, mess_compl
nastroi = 8
mess_compl = [False, 0]
cursor_n.execute("SELECT id FROM note ORDER BY id")

try:
	id_n = cursor_n.fetchall()[-1][0]
except:
	id_n = 0

async def Sender(msg):
	for guild in client.guilds:
		if str(guild) == "Liza":
			for channel in guild.channels:
				if str(channel) == "основной":
					await channel.send(msg)
	return





@client.event
async def on_ready():
	if log:
		print('ok')

	await Sender("Я запустилась!")

	#await message.channel.send("Я онлайн)")


''' 
команда которая не хочет работать
@client.command(pass_context = True)
async def hello(ctx):
	await ctx.send('Привет! Я запустилась')
'''


@client.event
async def on_message(message):
	global cnl
	global id_n
	global log
	global nastroi
	aut = str(message.author)
	
	if aut == "liza#5948":
		if log:
			print("[log] Message not used")
		return
	if cnl[0][0]:
		cursor_n.execute(f"INSERT INTO note VALUES (?, ?, ?, ?, ?)", (id_n+1, message.content.lower(), time.time(), 2*60*60+time.time(), 4))
		notes_c.commit()
		id_n = id_n + 1
		await message.channel.send("Запомнила)")
		cnl[0][0] = False
		return


# Get command and swich commad's program
	msg = message.content.lower()

#--------------------------------------------------------------------prl
	if msg =="отмена" and cnl[0][0]:
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
		return
#--------------------------------------------------------------------prl

	if log:
		print("[log] Message from " + aut + " : " + str(msg) + " used")

	if msg == "log!":
		log = not log
		if log:
			await message.channel.send("Логирование включено!")
		else:
			await message.channel.send("Логирование отключено!")

	if mess_compl[0] == True:
		if msg == "да":
			#cursor_n.execute(f"UPDATE complete SET 0 FROM note WHERE id = (?)", (mess_compl[1]))
			#notes_c.commit()
			pass
		return


	coman = swich(msg,opts,log = log)#-------------------------------swich(msg)

	if count(aut, ignor):  #sorry()
		if coman == "sor":
			ignor.remove(aut)
			await message.channel.send(str(ansr[coman][random.randint(0, len(ansr[coman]))]))
			return
		return

	if log:
		print("[log] Comand bot: " + str(coman))

	if coman == "prl":
		await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
		protocol[0][0] = True
		if log:
			print(protocol)
		return

	if coman == "nyd": #день
		if log:
			print("NYD start")

		cursor_n.execute("SELECT * FROM note ORDER BY time")
		id_n = cursor_n.fetchall()

		for i in range(len(id_n)):
			if int(id_n[i][2])>(time.time()-60*60*24):
				id_nt = time.localtime(int(id_n[i][2]))

				if log:
					print("[Log] note: "+ id_n[i][1])

				await message.channel.send("Заметка от "+str(id_nt.tm_mday)+"."+str(id_nt.tm_mon)+"."+str(id_nt.tm_year)+" "+str(id_nt.tm_hour)+":"+str(id_nt.tm_min)+" Текст: "+str(id_n[i][1]))

		await message.channel.send("Это все заметки за последние сутки")
		return

	if coman == "nyw":  #неделя
		cursor_n.execute("SELECT * FROM note ORDER BY time")
		id_n = cursor_n.fetchall()
		await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
		for i in range(len(id_n)):
			if int(id_n[i][2]) > (time.time() - 60 * 60 * 24*7):
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
		await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
		hello_log.append(aut)


		#engine.say("привет мир")
		#engine.runAndWait()
		return

	if coman == "hay":
		await message.channel.send(ansr[coman+str(int(nastroi/2))][random.randint(0, len(ansr[coman+str(int(nastroi/2))]))])
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
		await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
		return

	if coman == "htr":
		rez = 2#htr()  # ставить_чайник()

		if rez == 0:
			await message.channel.send("Не могу, не получается открыть COM порт(")
			return
		if rez == 1:
			await message.channel.send("COM порт открыла, но не получается отправить данные")
			return
		if rez == 2:
			await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))]) #random(0,int(len(ansr["htr"])))
			return
		return

	if coman == "gdb":
		await message.channel.send("Good bye)")
		exit()

	if coman == "msc":
		await message.channel.send("Включаю музыку")
		await message.channel.send("Не забудь проапгрейдить эту функцию у меня. Я хочу знать что ты хочешь послушать, а не включать все подряд")
		#включать_музыку()
		return
		
	if coman == "wth":
		#получить_и_сказать погоду()
		await message.channel.send("Поидее я должна сказать погоду, но мой создатель - ленивая жопа и не прикрутил мне эту функцию")
		return

	if coman == "rfl":
		await message.channel.send("Я пока не имею чувства юмора")
		await message.channel.send("Но если меня научат смеятся то я буду смеятся над тобой)")
		return

	if coman == "ntp":
		await message.channel.send("Что мне напомнить тебе?")
		cnl[0][0] = True
		return

	if coman == "lht":
		rez = 2# lht()  # свет()

		if rez == 0:
			await message.channel.send("Не могу, не получается открыть COM порт(")
			return
		if rez == 1:
			await message.channel.send("COM порт открыла, но не получается отправить данные")
			return
		if rez == 2:
			await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
			return
		return

	if coman == "lto":
		rez = 2# lto()  # свет()

		if rez == 0:
			await message.channel.send("Не могу, не получается открыть COM порт(")
			return
		if rez == 1:
			await message.channel.send("COM порт открыла, но не получается отправить данные")
			return
		if rez == 2:
			await message.channel.send(ansr[coman][random.randint(0,len(ansr[coman]))])
			return
		return

async def budos():
	global mess_compl
	if log:
		print("[Log] Budos start")
	while True:
		await asyncio.sleep(1320)
		#time.sleep(1320)

		if log:
			print("[Log] New loop budos")

		cursor_n.execute("SELECT * FROM note ORDER BY time")
		id_f = cursor_n.fetchall()
		for i in range(len(id_f)):
			if int(id_f[i][4]) != 0:
				id_ft = time.localtime(int(id_f[i][3]))#budos
				if id_ft < time.time():
					text = "Заметка на "+ str(id_ft.tm_mday) + "." + str(id_ft.tm_mon) + "." + str(id_ft.tm_year) + " " + str(id_ft.tm_hour) + ":" + str(id_ft.tm_min) + " Текст: " + str(id_n[i][1]) + "\n Выполнена?"
					await Sender(text)
					mess_compl[0]=True
					mess_compl[1]=int(id_f[i][0])
					break
				if id_ft < time.time()+60*60*2:
					text = "Заметка на " + str(id_ft.tm_mday) + "." + str(id_ft.tm_mon) + "." + str(id_ft.tm_year) + " " + str(id_ft.tm_hour) + ":" + str(id_ft.tm_min) + " Текст: " + str(id_n[i][1]) + "\nНе забудь!!!"
					await Sender(text)
					break



client.loop.create_task(budos())

token = open('token.txt', 'r').readline()
client.run(token)