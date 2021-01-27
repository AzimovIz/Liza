#import pyttsx3
import sqlite3
import time
import random

from discord.ext import commands

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

cursor_n.execute("SELECT id FROM note ORDER BY id")

try:
	id_n = cursor_n.fetchall()[-1][0]
except:
	id_n = 0

@client.event
async def on_ready():
	
	if log:
		print('ok')
	#await ctx.send('Хай, я онлайн!')


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
#-------------------------------------------------------------------prl

	if log:
		print("[log] Message from " + aut + " : " + str(msg) + " used")

	if msg == "log!":
		log = not log
		if log:
			await message.channel.send("Логирование включено!")
		else:
			await message.channel.send("Логирование отключено!")
		
	coman = swich(msg,opts,log = log)

	if count(aut, ignor):
		if coman == "sor":
			ignor.remove(aut)
			await message.channel.send(str(ansr[coman][random.randint(0, len(ansr[coman]))]))
			return
		return


	if log:
		print("[log] Comand bot: " + str(coman))

	if coman == "prl":
		await message.channel.send(str(ansr[coman][random.randint(0, len(ansr[coman]))]))
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

	if coman == "nyw":  #неделя
		cursor_n.execute("SELECT * FROM note ORDER BY time")
		id_n = cursor_n.fetchall()

		for i in range(len(id_n)):
			if int(id_n[i][2]) > (time.time() - 60 * 60 * 24*7):
				id_nt = time.localtime(int(id_n[i][2]))

				if log:
					print("[Log] note: " + id_n[i][1])

				await message.channel.send("Заметка от " + str(id_nt.tm_mday) + "." + str(id_nt.tm_mon) + "." + str(id_nt.tm_year) + " " + str(id_nt.tm_hour) + ":" + str(id_nt.tm_min) + " Текст: " + str(id_n[i][1]))

		await message.channel.send("Это все заметки за последнюю неделю")

		
	if coman == "hello":
		f = count(aut, hello_log)
		if f > 2:
			await message.channel.send("Ты меня бесишь! Я не буду тебе отвечать пока не извинишься!")
			ignor.append(str(message.author))
			return

		if f > 1:
			await message.channel.send("Ты что тупой? Перестань писать это!")
			hello_log.append(str(message.author))
			return

		if str(message.author) in hello_log:
			await message.channel.send("Я уже здоровалась с тобой, меня этим не возмешь.")
			hello_log.append(str(message.author))
			return
		await message.channel.send(str(ansr[coman][random.randint(0, len(ansr[coman]))]))
		hello_log.append(str(message.author))


		#engine.say("привет мир")
		#engine.runAndWait()
		return

	if coman == "me":
		await message.channel.send("Меня зовут Лиза и это мой сервер.\n Сдесь я обрабатываю запросы от Username(он мой создатель) и отвечаю на них.\n Все это связано с автоматизацией дома и я занимаюсь тем что слежу за состоянием всего и выполняю разные действия по типу 'поставить чайник' или 'проверь не забыл ли я закрыть дверь' такое вот. \n Робоприслуга вобщем хотя мне и не нравится это выражение.")
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
			await message.channel.send(str(ansr[coman][random.randint(0,len(ansr[coman]))])) #random(0,int(len(ansr["htr"])))
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

	if coman == "ntr":
		pass




token = open('token.txt', 'r').readline()
client.run(token)