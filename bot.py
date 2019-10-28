import telebot
from telebot import types
from pytube import YouTube
import moviepy.editor as mp
import os
import time
from flask import Flask,request
import json


secret = "SECRET"
token = 'Token'
bot = telebot.TeleBot(token, threaded=False)

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://Username.pythonanywhere.com/{}".format(secret))

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


class Clip(object):
	url = ''
	res = ''
	c_type = ''
clip = Clip()

# Удаление скачанных файлов
def delete_clip(path):
	for p in path:
		if os.path.isfile(p):
			os.remove(p)
		else:
			print('error file')

# Изменнение положения пользователя
def change_step(user_id,step):
	with open('data.json','r') as file_read:
		data = json.load(file_read)
		data[user_id][0] = str(step) 
		with open('data.json','w') as write_file:
			json.dump(data, write_file)


#Последнее сообщение

def change_lastmess_id(user_id,message_id):
	with open('data.json','r') as file_read:
		data = json.load(file_read)
		data[user_id+' mess_id'] = str(message_id)
		with open('data.json','w') as write_file:
			json.dump(data, write_file)


# Загрузка положения бота
def bot_load(message):
	with open('data.json','r') as file_read:
		data = json.load(file_read)
		if str(message.from_user.id) not in data:
			data[str(message.from_user.id)][0] = '0' 
			with open('data.json','w') as write_file:
				json.dump(data, write_file)
		else:
			if data[str(message.from_user.id)] == '0':
				msg = bot.send_message(message.from_user.id,'Hello')
				bot.register_next_step_handler(msg,hello_mess)

			if data[str(message.from_user.id)][0] == '1':
				msg = bot.send_message(message.from_user.id,'Please send me , URL !')
				bot.register_next_step_handler(msg,URL_get)

			if data[str(message.from_user.id)][0] == '2':
				markup = types.ReplyKeyboardMarkup()
				btn_mp4 = types.KeyboardButton('mp4')
				btn_mp3 = types.KeyboardButton('mp3')
				btn_not = types.KeyboardButton('Cancel')

				markup.row(btn_mp4)
				markup.row(btn_mp3)
				markup.row(btn_not)

				msg = bot.send_message(message.from_user.id,'Choose the Type video: ',reply_markup=markup)

				bot.register_next_step_handler(msg,get_type)

			with open('data.json','w') as write_file:
				json.dump(data, write_file)

#тесты

'''

with open('data.json','r') as file_read:
	data = json.load(file_read)
	for userid in data:
		chat = bot.get_chat(userid[1])
		
'''
#----

@bot.message_handler(func= lambda message:True)
def load_user(message):
	bot_load(message)

#----
@bot.message_handler(commands=['start'])
def hello_mess(message):
	with open('data.json','r') as file_read:
		data = json.load(file_read)
		if str(message.from_user.id) not in data:
			data[str(message.from_user.id)] = ['0',str(message.chat.id)]
			 
			with open('data.json','w') as write_file:
				json.dump(data, write_file)
		else:
			data[str(message.from_user.id)] = ['0',str(message.chat.id)] 
			with open('data.json','w') as write_file:
				json.dump(data, write_file)

	msg = bot.send_message(message.from_user.id, 'Please send me , URL !')

	bot.register_next_step_handler(msg, URL_get)


def URL_get(message):
	change_step(message.from_user.id, '1')
	change_lastmess_id(message.from_user.id, message.message_id)

	clip.url=str(message.text)

	markup = types.ReplyKeyboardMarkup()
	btn_mp4 = types.KeyboardButton('mp4')
	btn_mp3 = types.KeyboardButton('mp3')
	btn_not = types.KeyboardButton('Cancel')

	markup.row(btn_mp4)
	markup.row(btn_mp3)
	markup.row(btn_not)

	msg = bot.reply_to(message,'Choose the Type video: ',reply_markup=markup)

	bot.register_next_step_handler(msg,get_type)


def get_type(message):
	clip.c_type = message.text
	change_lastmess_id(message.from_user.id, message.message_id)
	change_step(message.from_user.id, '2')


	if str(message.text) == 'mp4':
		try:
		    yt = YouTube(clip.url)
		    title = yt.title.replace('.', '').replace('|', "")
		    path =title+'.mp4'
		    path2 = title+'.mp3'
		    bot.send_message(message.from_user.id, 'Download Video...')

		    yt.streams.filter(file_extension='mp4',resolution='360p').first().download()

		    video = open(path,'rb')
		    bot.send_message(message.from_user.id, 'Sending Video...')
		    bot.send_video(message.from_user.id, video)
		    video.close()

		    bot.send_message(message.from_user.id, title+'-DONE!')

		    time.sleep(1)
		    delete_clip([path])
		    msg = bot.send_message(message.from_user.id, 'Please send me , URL !')
		    bot.register_next_step_handler(msg, URL_get)

		except pytube.exceptions.VideoUnavailable:
			msg = bot.send_message(message.from_user.id,'This video Unavailable. Send other URL!')
			bot.register_next_step_handler(msg,URL_get)




	elif str(message.text) == 'mp3':
		try:
			yt = YouTube(clip.url)

			title = yt.title.replace('.', '').replace('|', "")
			path =title+'.mp4'
			path2 = title+'.mp3'

			bot.send_message(message.from_user.id, 'Download Audio...')

			yt.streams.filter(file_extension='mp4',resolution='360p').first().download()
			audioclip = mp.AudioFileClip(path).write_audiofile(path2)

			audio = open(path2,'rb')

			bot.send_message(message.from_user.id, 'Sending Audio...')
			bot.send_audio(message.from_user.id,audio)
			audio.close()

			bot.send_message(message.from_user.id, title+'''-DONE!
			Donat Me:
			Visa: MY CARD(4276 6000 5009 1996)''')

			time.sleep(1)
			delete_clip([path,path2])
			msg = bot.send_message(message.from_user.id, 'Please send me , URL !')
			bot.register_next_step_handler(msg, URL_get)

		except pytube.exceptions.VideoUnavailable:
			msg = bot.send_message(message.from_user.id,'This video Unavailable. Send other URL!')
			bot.register_next_step_handler(msg,URL_get)
			bot.register_next_step_handler(msg, URL_get)

	elif str(message.text)=='Cancel':
	    msg = bot.send_message(message.from_user.id, 'Please send me , URL !')
	    bot.register_next_step_handler(msg, URL_get)

	else:
		msg = bot.send_message(message.from_user.id, 'Please Choose correct answer!')
		bot.register_next_step_handler(msg, URL_get)

def get_res(message):

	clip.res = str(message.text)
	print(clip.res)
	yt = YouTube(str(clip.url))
	title = yt.title.replace('.', '').replace('|', "")

	stream = yt.streams.filter(file_extension='mp4',resolution=str(clip.res)).first()
	path =title+'.mp4'
	path2 = title+'.mp3'
	stream.download()
	video = open(path,'rb')
	bot.send_video(message.from_user.id,video)
	video.close()

	time.sleep(1)
	delete_clip([path])






'''
	stream = YouTube(str(message)).streams.filter(file_extension='mp4').first()
	yt = YouTube(str(message))
	path = 'C:/Users/Rizvan/Desktop/Python/Apple_Bot/'+str(yt.title)+'.mp4'
	path2 = 'C:/Users/Rizvan/Desktop/Python/Apple_Bot/'+str(yt.title)+'.mp3'
	#stream.download()
	#video = open(path,'rb')


	yt.streams.filter(only_audio=True).first().download()
	audioclip = mp.AudioFileClip(path).write_audiofile(path2)
	audio = open(path2,'rb')

	bot.send_audio(message.from_user.id,audio)
	'''