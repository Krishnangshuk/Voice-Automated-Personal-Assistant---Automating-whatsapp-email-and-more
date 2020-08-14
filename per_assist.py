import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
from pynput.keyboard import Key, Controller
import time
import calendar
from googletrans import Translator
import requests
import json
import os
from PyDictionary import PyDictionary
import smtplib
from email.message import EmailMessage
import imghdr
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

dictionary=PyDictionary()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
keyboard=Controller()
chrome='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
engine.setProperty('voice',voices[1].id) 

def wakeup(text):
	wake_words=['hey death','ok death','hay death','hi death']
	for phrase in wake_words:
		if phrase in text:
			return True
	return False

def speak(audio):
	engine.say(audio)
	engine.runAndWait()
	print(audio) 


def wish():
	hour= int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("Good Morning Sir")
	elif hour>=12 and hour<18:
		speak("Good Afternoon Sir")
	else:
		speak("Good Evening Sir")

def command():
	r=sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		speak("speak")
		audio=r.listen(source)
		try:
			comm=r.recognize_google(audio, language='en-in')
			print(f"You said {comm}\n")
		except:
			return "None"
	return comm

def location():
	r=requests.get('https://get.geojs.io/')
	ip_request= requests.get('https://get.geojs.io/v1/ip.json')
	ip= ip_request.json()['ip']
	url=f'https://get.geojs.io/v1/ip/geo/{ip}.json'
	loc_request= requests.get(url)
	loc=loc_request.json()
	return loc

def open_folder(): 
	speak("Specify the drive to search for the desired file.....say first for d drive...second for e drive...and third. for c drive")
	temp=command().lower()
	if temp =='first' :
		dir_path="d:"
	elif temp =='second' :
		dir_path="e:"
	elif temp =='third' :
		dir_path="c:"
	speak("Now...Please say the name of the folder and sub folders..after every time i say speak .....and say done when you have finished saying the path of the folder")
	while True:
		temp=command().lower()
		if temp=='done':
			break
		dir_path=dir_path+f'//{temp}'
	return dir_path

def open_file():
	dir_path=open_folder()
	speak("Whats the name of the file that you want to open?")
	temp=command()
	l=os.listdir(dir_path)
	for x in l:
		name=x.split('.')[0]
		if name==temp:
			name=name+'.'+x.split('.')[1]
			dir_path=dir_path+'//'+name
			break
	return dir_path,name


if __name__ == "__main__":
	start_com=command().lower()
	if wakeup(start_com)==True:
		wish()
		while True:
			com=command().lower() 
			if 'google' in com:
				speak("Opening Google......")
				webbrowser.get(chrome).open("google.com")
			elif 'search' in com:
				webbrowser.get(chrome).open("google.com")
				speak("Opening Google......") 
				com= com.replace("search", "")
				time.sleep(0.05)
				for char in com:
					keyboard.press(char)
					keyboard.release(char)
					time.sleep(0.05)
					time.sleep(0.05)
				keyboard.press(Key.enter)
				keyboard.release(Key.enter)
			elif 'youtube' in com: 
				speak("Opening youtube......") 
				webbrowser.get(chrome).open("youtube.com")
			elif 'what day is it' in com:
				my_date=datetime.datetime.today()
				weekday= calendar.day_name[my_date.weekday()]
				speak(f"Today is {weekday}")
			elif 'translate' in com:
				speak("To which language Sir")
				tran_lang=command()
				translator= Translator()
				speak("Whats the text")
				text= command()
				translation = translator.translate(text, dest=tran_lang, src= 'en')
				speak(translation.text)
			elif 'weather' in com:
				loc=location()
				city=loc['city']
				url=f"https://openweathermap.org/data/2.5/weather?q={city}&appid=your app id"
				res= requests.get(url)
				output= res.json()
				weather_status=output['weather'][0]['description']
				temperature= output['main']['temp']
				humidity= output['main']['humidity']
				wind_speed= output['wind']['speed']
				speak(f"The weather status in {city}.... is {weather_status} with a tempertaure of {temperature} degree Celcius..... humidity of {humidity}%.... and wind speed of {wind_speed} kilometers per hour")
			elif 'location' in com:
				loc=location()
				speak(f"You are currently in the city {loc['city']}... situated in {loc['region']}....{loc['country']}")
			elif 'who are you' in com:
				speak("I am a virtual assistant coded in python...named Death.... How can i help you?")
			elif 'open folder' in com:
				dir_path=open_folder()
				os.startfile(dir_path)
			elif 'open file' in com:
				dir_path,file_name= open_file()
				speak(f"opening {file_name}")
				os.startfile(dir_path)
			elif 'type some text' in com:
				speak("Sure. why not!")
				while True:					
					text= command()
					if text=='done':
						break
					elif text=='next line':
						keyboard.press(Key.enter)
						keyboard.release(Key.enter)
					for char in text:
						keyboard.press(char)
						keyboard.release(char)
						time.sleep(0.05)
			elif 'dictionary' in com:
				speak("Whats the word Sir?")
				word=command()
				res=dictionary.meaning(word)
				speak(res)
			elif 'email' in com:
				msg=EmailMessage()
				speak("Please give the information for sending the email..as per instructions...")
				speak("Whats the subject?")
				sub=command()
				speak("Who do you want to send the email to?..Please type the email id")
				to=input("Email:")
				msg['Subject']= sub
				msg['From']='pasujoy141@gmail.com'
				msg['to']=to
				speak("Whats the message you want to send?")
				text=command()
				msg.set_content(text)
				speak("Do you want to attach any file to the email?...Answer with a yes or no")
				response=command().lower()
				if response=='yes':
					dir_path,file_name= open_file()
					with open(dir_path,'rb') as file:
						file_data=file.read()
						file_type=imghdr.what(file.name)
					speak("Is it an image file?..Answer with a yes or no")
					resp=command().lower()
					if resp=='yes':
						main_type='image'
						sub_type=file_type
					else :
						main_type='application'
						sub_type='octet-stream'
					msg.add_attachment(file_data,maintype=main_type,subtype=sub_type,filename=file_name)
				else:
					pass
				with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
					smtp.login('your email','your password')
					smtp.send_message(msg)
				speak("The mail has been sent")
			elif 'whatsapp' in com:
				speak("Whats the name of the contect to whom the message will be sent")
				name=input("Name:")
				speak("Whats the message?")
				msg=command()
				speak("Please be ready to scan the qr code of whatsapp web")
				driver = webdriver.Chrome()
				driver.get('https://web.whatsapp.com/')
				time.sleep(15)
				user = driver.find_element_by_xpath("//span[@title = '{}']".format(name))
				user.click()
				msg_box = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
				msg_box.send_keys(msg)
				button = driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
			elif 'stop' in com:
				break




my name is RohitNonestopNonestop

