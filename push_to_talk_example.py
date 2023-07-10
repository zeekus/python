#!/usr/bin/python
#filename: push_to_talk_example.py
#description: push to talk voice recognition with python

import importlib

try:
    sr = importlib.import_module('speech_recognition')
    print("speech module is loaded")
except ImportError:
    print('speech module is not loaded')

try:
    keyboard = importlib.import_module('keyboard')
except: 
    print ('keyboard module is not loaded.')

#import speech_recognition as sr
#import keyboard

# Initialize the recognizer
recognizer = sr.Recognizer()

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("Recognized text:", text)
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))

# Main loop
while True:
    # Check if the ~ key is pressed
    if keyboard.is_pressed('~'):
        recognize_speech()
