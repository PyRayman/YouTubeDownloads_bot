import telebot
from telebot import types
from pytube import YouTube
import moviepy.editor as mp
import os
import time
from flask import Flask,request


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


def delete_clip(path):
	for p in path:
		if os.path.isfile(p):
			os.remove(p)
		else:
			print('error file')


@bot.message_handler(commands=['start'])
def hello_mess(message):
	msg = bot.send_message(message.from_user.id, 'Please send me , URL !')

	bot.register_next_step_handler(msg, URL_get)


def URL_get(message):
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

	if str(message.text) == 'mp4':
	    yt = YouTube(clip.url)
	    title = yt.title.replace('.', '').replace('|', "")
	    path =title+'.mp4'
	    path2 = title+'.mp3'
	    bot.send_message(message.from_user.id, 'Download Video...')

	    yt.streams.filter().first().download()

	    video = open(path,'rb')
	    bot.send_message(message.from_user.id, 'Sending Video...')
	    bot.send_video(message.from_user.id, video)
	    video.close()

	    bot.send_message(message.from_user.id, title+'-DONE!')

	    time.sleep(5)
	    delete_clip([path])
	    msg = bot.send_message(message.from_user.id, 'Please send me , URL !')
	    bot.register_next_step_handler(msg, URL_get)



	elif str(message.text) == 'mp3':
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

		time.sleep(5)
		delete_clip([path,path2])
		msg = bot.send_message(message.from_user.id, 'Please send me , URL !')
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