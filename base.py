import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
from pocketsphinx import LiveSpeech
#from playsound import playsound

import os
import sys
import subprocess
#from pathlib import Path
import ctypes
import linecache

import math
import time
import datetime
import calendar

import wikipedia
#import wikiquote
import webbrowser
#import smtplib
#import requests
#import json
#from urllib.request import urlopen

#from selenium import webdriver
#import wolframalpha
#from twilio.rest import Client

import pyautogui as pag
import random
#import pyjokes
import win32clipboard as wc

#import wmi
#import getpass
#from comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#import winshell
#from ecapture import ecapture as ec

import tkinter as tk
from PIL import ImageTk, Image
import threading
#import multiprocessing

#import num2words
#import word2number

#from Scripts.vcs import vCube
#from Scripts.hexon import run_hexon
#from Scripts.clock import run_clock


class Base:
    #Conversion dictionaries and lists
    WORD_TO_NUM = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                   'eight': '8',
                   'nine': '9', 'zero': '0'}

    WORD_TO_SYM = {'dot': '.', 'full stop': '.', 'exclamation mark': '!', 'at': '@', 'hash tag': '#', 'dollar': '$',
                   'percent': '%', 'percentage': '%', 'modulus': '%', 'asterisk': '*', 'times': '*', 'and': '&',
                   'close parenthesis': ')', 'question mark': '?', 'open bracket': '{', 'close bracket': '}',
                   'open square bracket': '[', 'close square bracket': ']', 'slash': '/', 'backslash': '\\',
                   'plus': '+', 'pipe': '|', 'open parenthesis': '(', 'underscore': '_', 'equals': '=', 
                   'equals to': '=', 'minus': '-', 'hyphen': '-', "space bar": " ", "new line": "\n"}

    #MONTHS = (None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
    #       'November', 'December')
    MONTHS = calendar.month_name

    #DAYS = calendar.day_name
    #DAYS = tuple([DAYS[-1]] + DAYS[:-1])
    DAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')

    PARTIAL_DATES = {1: '1st', 2: '2nd', 3: '3rd', 21: '21st', 22: '22nd',
                     23: '23rd', 31: '31st'}

    CREATED = datetime.datetime(2020, 1, 10)

    CWD = os.getcwd()

    VOICE_DICT = {'male': 0, 'boy': 0, 'female': 1, 'girl': 1}

    EXTENSIONS = {"HTML": [".html5", ".html", ".htm", ".xhtml"],
                  "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
                             ".heif", ".psd"],
                  "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
                             ".qt", ".mpg", ".mpeg", ".3gp", ".mkv"],
                  "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                                ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                                ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt",
                                "pptx"],
                  "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                               ".dmg", ".rar", ".xar", ".zip"],
                  "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
                            ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
                  "PLAINTEXT": [".txt", ".in", ".out"],
                  "PDF": [".pdf"],
                  "PYTHON": [".py"],
                  "XML": [".xml"],
                  "EXE": [".exe"],
                  "SHELL": [".sh"]}

    FILE_FORMATS = {'.html5': 'HTML', '.html': 'HTML', '.htm': 'HTML', '.xhtml': 'HTML',
                    '.jpeg': 'IMAGES', '.jpg': 'IMAGES', '.tiff': 'IMAGES',
                    '.gif': 'IMAGES', '.bmp': 'IMAGES', '.png': 'IMAGES',
                    '.bpg': 'IMAGES', 'svg': 'IMAGES', '.heif': 'IMAGES', '.psd': 'IMAGES',
                    '.avi': 'VIDEOS', '.flv': 'VIDEOS', '.wmv': 'VIDEOS', '.mov': 'VIDEOS',
                    '.mp4': 'VIDEOS', '.webm': 'VIDEOS', '.vob': 'VIDEOS', '.mng': 'VIDEOS',
                    '.qt': 'VIDEOS', '.mpg': 'VIDEOS', '.mpeg': 'VIDEOS', '.3gp': 'VIDEOS', '.mkv': 'VIDEOS',
                    '.oxps': 'DOCUMENTS', '.epub': 'DOCUMENTS', '.pages': 'DOCUMENTS',
                    '.docx': 'DOCUMENTS', '.doc': 'DOCUMENTS', '.fdf': 'DOCUMENTS',
                    '.ods': 'DOCUMENTS', '.odt': 'DOCUMENTS', '.pwi': 'DOCUMENTS',
                    '.xsn': 'DOCUMENTS', '.xps': 'DOCUMENTS', '.dotx': 'DOCUMENTS',
                    '.docm': 'DOCUMENTS', '.dox': 'DOCUMENTS', '.rvg': 'DOCUMENTS',
                    '.rtf': 'DOCUMENTS', '.rtfd': 'DOCUMENTS', '.wpd': 'DOCUMENTS',
                    '.xls': 'DOCUMENTS', '.xlsx': 'DOCUMENTS', '.ppt': 'DOCUMENTS', 'pptx': 'DOCUMENTS',
                    '.a': 'ARCHIVES', '.ar': 'ARCHIVES', '.cpio': 'ARCHIVES', '.iso': 'ARCHIVES',
                    '.tar': 'ARCHIVES', '.gz': 'ARCHIVES', '.rz': 'ARCHIVES', '.7z': 'ARCHIVES',
                    '.dmg': 'ARCHIVES', '.rar': 'ARCHIVES', '.xar': 'ARCHIVES', '.zip': 'ARCHIVES',
                    '.aac': 'AUDIO', '.aa': 'AUDIO', '.dvf': 'AUDIO', '.m4a': 'AUDIO', '.m4b': 'AUDIO',
                    '.m4p': 'AUDIO', '.mp3': 'AUDIO', '.msv': 'AUDIO', 'ogg': 'AUDIO', 'oga': 'AUDIO',
                    '.raw': 'AUDIO', '.vox': 'AUDIO', '.wav': 'AUDIO', '.wma': 'AUDIO', '.txt': 'PLAINTEXT',
                    '.in': 'PLAINTEXT', '.out': 'PLAINTEXT', '.pdf': 'PDF', '.py': 'PYTHON', '.xml': 'XML',
                    '.exe': 'EXE', '.sh': 'SHELL'}
    '''
    FILE_FORMATS = {file_format: directory
                    for directory, file_formats in EXTENSIONS.items()
                    for file_format in file_formats}
    '''
    '''
    SORRY_MESSAGES = ('I am sorry, I could not understand that', 'Oh oh',
                        'I am afraid, I can\'t talk about that', 'Why do you want that?',
                        'I am thinking but this beats me...', 'Allright allright, I give up', 'Who knows',
                        'Don\'t get me wrong but I don\'t know all the answers',
                        'Hey, why don\'t you ask me another question while I think more about that?',
                        'Believe me I am trying but, I simply could not answer that')
    EXIT_MESSAGES = ('exit', 'terminate', 'go away', 'bored', 'enough', 'quit')
    POSITIVE_ANSWERS = ('Yes', 'Of course', 'Definitely')
    NEGATIVE_ANSWERS = ('No', 'Nope', "I don't think so", 'Sorry')
    SELF_MESSAGES = ('you', 'yourself')
    MASTER_MESSAGES = ('me', 'myself', 'I')
    RUDIMENTARY_QUESTION_TAGS = ('who', 'why', 'when', 'where', 'what', 'which', 'how')
    '''


    def __init__(self):
        self.status = {'run': True, 'nss_open': False, 'get_cmd_func': None, 'mode': 'efficiency'} 
        #, 'get_cmd_queue': []}
        #mode -> normal/efficiency

        self.action = 'normal' 
        #normal/[code(py)/code(java)/code(c++)/code(c)]

        try:
            raise Exception() #debugging pupose - remove this
            with open(f'{self.CWD}\\cache.cache', 'r') as file:
                self.cache = eval(file.read())

            self.info, self.dirs, self.api_keys, self.remainders, self.todo = self.cache

        except:
            self.cache = None

            self.info = {'name': 'centrix', 'master': 'Jaiwanth', 'mode': 'text', 'version': '0.4.7',
                         'number lock': False, 'symbol lock': False, 'say': True, 'voice': 'male',
                         'recognition': 'offline1', 'email': 'jaiwanthkarthi@gmail.com', 'pass': '********',
                         'read rate': 128, 'speak rate': 150, 'wikipedia sentences': 2, 'keyboard type': False, 
                         'mimic': False, 'current directory':  self.CWD, 'file find': [False, True, False, False],
                         'twilio_send_no': '1234', 'twilio_rec_no': '5678'}

            #Diretories to systems and dependencies
            self.dirs = {'output': 'D:/Users/CoderAlpha/Desktop',
                         'model': 'D:/Users/CoderAlpha/Documents/Prog/Python/py_proj/projectX/dependencies/Voice/vskTrials/model',
                         'dependencies': 'D:/Users/CoderAlpha/Documents/Prog/Python/py_proj/projectX/dependencies',
                         'chrome': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
                         'google': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
                         'cmd': 'C:/Windows/system32/cmd',
                         'songs': 'D:/Users/CoderAlpha/Music/Jai/Songs/Mp3 English',
                         'pics': 'D:/Users/CoderAlpha/Pictures/Pictures/Other pictures/Other Photograpy',
                         'control panel': 'C:/Windows/System32/control.exe',
                         'task_manager': 'C:/Windows/system32/Taskmgr.exe',
                         'word': 'C:/Program Files/Microsoft Office/root/Office16/WINWORD.exe',
                         'powerpoint': 'C:/Program Files/Microsoft Office/root/Office16/POWERPNT.exe',
                         'excel': 'C:/Program Files/Microsoft Office/root/Office16/EXCEL.exe',
                         'vs_code': 'C:/Users/CoderAlpha/AppData/Local/Programs/Microsoft VS Code/Code.exe',
                         'python': 'C:/Users/CoderAlpha/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Python 3.8/IDLE (Python 3.8 64-bit).lnk',
                         'pycharm': 'C:/Program Files/JetBrains/PyCharm Community Edition 2019.3.3/bin/pycharm64'}

            #Api keys to online data forums
            self.api_keys = {'wolframalpha': None, 'openWeather': None, 'timesOfIndia': None,
                         'googleNews': None, 'bbc': None, 'twilio': [None, None]}

            self.remainders = {}
            self.todo = []

        #Text-To-Speech initialization
        self.ENGINE = pyttsx3.init('sapi5')
        self.VOICES = self.ENGINE.getProperty("voices")
        #self.ENGINE.setProperty('voice', self.VOICES[self.info['voice']].id)
        self.ENGINE.setProperty('rate', self.info['speak rate'])
        #self.ENGINE.setProperty('volume', 1)

        #voice vars
        self.model, self.rec, self.p, self.stream = None, None, None, None
        self.offline2_iterator = iter(LiveSpeech())

        #Interface vars
        self.geometry = (650, 350, 50, 50)
        self.nss_geometry = (650, 350, 50, 50)

    def remember(self):
        with open(f'{self.CWD}\\cache.cache', 'w') as file:
            file.write(f'({self.info}, {self.dirs}, {self.api_keys}, {self.remainders}, {self.todo})')

    #-----------------------Sub-Helpers------------------------------------

    @staticmethod
    def hook_to_thread(func):
        def inner_func(*args, **kwargs):
            threading.Thread(target=func).start()#, args=(*args), kwargs=(**kwargs)).start()

        return inner_func

    @staticmethod
    def hook_to_multiprocess(func):
        def inner_func(*args, **kwargs):
            multiprocessing.Process(target=func).start()#, args=(*args), kwargs=(**kwargs)).start()

        return inner_func
        
    @staticmethod
    def printException():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        sys.stderr.write('\nERROR:-\n{}, \nLINE {} \n"{}"\n<{}>\n\n'.format(filename, lineno, line.strip(), exc_obj))

    @staticmethod
    def checkInternet():
        try:
            wikipedia.summary('wikipedia', sentences=1)
            return True
        except:
            return False

    @staticmethod
    def searchList(listToSearchOn, stringToSearch):
        indexes = []
        for n in range(len(listToSearchOn)):
            if stringToSearch in listToSearchOn[n].lower():
                indexes.append(n)
        return indexes

    @staticmethod
    def get_dissected_query(query):
        d_query = query.split(' ')

        for n in range(len(d_query)):
            if d_query[n][0] in (',', '.'):
                d_query[n] = d_query[n][1:]
            if d_query[n][-1] in (',', '.'):
                d_query[n] = d_query[n][:-1]

        return d_query

    @staticmethod
    def inQuery(string, query):
        #if 'eff' in self.status['mode']:
        #    return (string in query)
        return (string in query)
        '''
        present = False
        indx = query.find(string)
        
        if indx == -1:
            return False
        
        try:
            present = (indx-1 == ' ')
        except:
            present = True

        try:
            return (query[indx+len(string)] == ' ' and present)
        except:
            return present
        '''

    @staticmethod
    def splitQuery(query, start=0, end=None):
        if not end:
            try:
                return query[start]
            except:
                return ''
        else:
            try:
                return query[start:end]
            except:
                return ''

    @staticmethod
    def searchDQuery(d_query, n, string):
        try:
            return (d_query[n] == string)
        except:
            return False

    @staticmethod
    def splitDQuery(d_query, n):
        try:
            return d_query[n:]
        except:
            return []

    @staticmethod
    def getClipData():  #Returns the most recently copied clipboard text
        wc.OpenClipboard()
        data = wc.GetClipboardData()
        wc.CloseClipboard()
        return data

    @classmethod
    def getDate(cls, change=False):
        t = datetime.datetime.now()
        month = t.month
        year = t.year
        day = t.day

        if not change:
            month = cls.MONTHS[month]
            m = t.month
            y = year

            try:
                date = cls.PARTIAL_DATES[day]
            except:
                date = str(day) + 'th'

        elif change == 'yesterday':
            day -= 1

            if day == 0:
                if month in (1, 3, 5, 7, 8, 10, 12):
                    day = 31
                elif month in (4, 6, 9, 11):
                    day = 30
                else:
                    if (year % 4) == 0:
                        day = 29
                    else:
                        day = 28
                month -= 1

            if month == 0:
                month = 12
                year -= 1

            month = cls.MONTHS[month]
            m = t.month
            y = year

            try:
                date = cls.PARTIAL_DATES[day]
            except:
                date = str(day) + 'th'

        elif change == 'tomorrow':
            day += 1

            if month in (1, 3, 5, 7, 8, 10, 12):
                if day == 32:
                    day = 1
                    month += 1
            elif month in (4, 6, 9, 11):
                if day == 31:
                    day = 1
                    month += 1
            else:
                if (year % 4) == 0:
                    if day == 30:
                        day = 1
                        month += 1
                else:
                    if day == 29:
                        day = 1
                        month += 1

            if month == 13:
                month = 1
                year += 1

            month = cls.MONTHS[month]
            m = t.month
            y = year

            try:
                date = cls.PARTIAL_DATES[day]
            except:
                date = str(day) + 'th'

        if m < 3:
            m += 12
            y -= 1

        m = 2 * m + (6 * (m + 1)) / 10
        y = y + (y / 4) + (y / 400) - (y / 100)
        dayIndex = int(day + m + y + 1) % 7

        return cls.DAYS[dayIndex], date, month, str(year)

    #----------------------------main helpers---------------------------

    def speak(self, text):  #Speaks a given string
        self.printSpeech(f'{text}')
        if self.info['say']:
            self.printStatus('Speaking...')
            self.ENGINE.say(text)
            self.update(check_alarm=False)

            self.ENGINE.runAndWait()
            self.emptyStatus()
            self.update(check_alarm=False)

    def wishMe(self): #Wishes the current master, in the given time
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            greet = 'Morning'
        elif 12 <= hour < 16:
            greet = 'Afternoon'
        elif 16 <= hour < 20:
            greet = 'Evening'
        else:
            greet = 'Night'

        self.speak(f"Good {greet} {self.info['master']}! I am {self.info['name'].upper()}... How may I help you?")

    def agree(self):  #Speaks a phrase of agreement
        agreeWords = ('Sure ', 'Definitely ', 'Absolutely ', 'Aye ', 'Yes ', 'Yep ',
                      'Sure thing ', 'Consider it done ', 'With pleasure ', 'Okay ',
                      'Copy that ', 'Doing it ')
        addressWords = ('Boss...', 'Captain...', self.info['master'] + '...')
        self.speak(random.choice(agreeWords) + random.choice(addressWords))

    def execProtocol(self, protocol):  #Executes a given protocol phrase
        if 'exit' in protocol:
            self.speak(random.choice(('Farewell ', 'Goodbye ', 'See you ', 'Bye ')) + self.info['master'] + '!')
            self.status['run'] = False
            self.close_interface()
        else:
            self.speak('Protocol not defined...')

    def takeCommand_Online1(self):  #Speech-To-Text with internet, uses online-1
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.printStatus('Listening...')
            audio = r.listen(source)
        try:
            self.printStatus('Recognizing...')
            return_query = r.recognize_google(audio, language='en-in')
            self.emptyStatus()
            #self.printOnConsole(f'{return_query}')
            return return_query
        except:
            self.printSpeech('Input not recognizable! Try again...')
            return ''

    def takeCommand_Offline1(self):  #Speech-To-Text with offline-1
        self.refresh_Offline1()
        self.printStatus('Listening for input...')
        while True:
            self.update()
            dat = self.stream.read(4000)
            if self.rec.AcceptWaveform(dat):
                return_query = (eval(self.rec.Result()))['text']
                if return_query == '' or return_query == ' ':
                    self.update()
                    continue
                #self.printOnConsole(f'{return_query}')
                self.emptyStatus()
                return return_query

    def takeCommand_Offline2(self): #Speech-To-Text with offline-2
        self.update()
        try:
            return str(next(self.offline2_iterator))
        except:
            self.offline2_iterator = LiveSpeech()
            self.update()
            return str(next(self.offline2_iterator))

    def runMain_Offline1(self):
        while (self.info['recognition'] == 'offline1') and self.status['run'] and (self.info['mode'] == 'audio'):
            #print('In VOICE main...')
            self.update()
            try:
                data = self.stream.read(4000)
                self.update()
                if self.rec.AcceptWaveform(data):
                    query = (eval(self.rec.Result()))['text']

                    if query == '' or query == ' ':
                        #self.printSpeech('Empty VOICE input...')
                        self.update()
                        continue

                    #query = self.formatQuery(query)
                    self.update()
                    self.processQuery(query)
                    self.printStatus('Listening to VOICE...')
            except:
                #self.printException()
                #print('Stream reload...')
                self.refresh_Offline1()
                continue

    def init_Offline1(self):
        #Offline speech-recognition initialization - takes roughly 30 seconds
        self.printStatus('Initializing VOICE dependencies...')
        self.speak('Initializing VOICE dependencies...')
        self.model = Model(self.dirs['model'])
        self.rec = KaldiRecognizer(self.model, 16000)
        self.p = pyaudio.PyAudio()
        self.refresh_Offline1()
        self.speak('VOICE Dependencies initialized...')

    def refresh_Offline1(self):
        self.update()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

    def recordVoice(self, filename):  #Records audio and saves it to a given filename
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.printStatus('Listening to record...')
            audio = r.listen(source)
            self.printStatus('Recording audio...')
        with open(f'{self.dirs["output"]}/{filename}.mp3', 'wb') as f:
            f.write(audio.get_wav_data())
        self.emptyStatus()
        self.speak(f'Audio Recorded in {filename}.mp3...')

    #Function to generally get an input from the user, based on recognition, mode and self
    def __getCommand_helper(self, failSafeFunc, finalBind):
        def bindFunc(event):
            queryData = self.formatQuery(self.queryVar.get())
            self.queryVar.set('')
            self.printOnConsole(queryData)
            failSafeFunc(queryData)
            if finalBind:
                self.bindQueryEntry('<Return>', self.evalQuery)

        if self.info['mode'] == 'audio':
            self.bindQueryEntry('<Return>', bindFunc)

            if self.info['recognition'] == 'online1':
                q = self.takeCommand_Online1()
            elif self.info['recognition'] == 'offline1':
                q = self.takeCommand_Offline1()
            elif self.info['recognition'] == 'offline2':
                q = self.takeCommand_Offline2()

            self.printOnConsole(q)
            self.bindQueryEntry('<Return>', self.evalQuery)
            return q

        else:
            self.bindQueryEntry('<Return>', bindFunc)
            return False

    def getCommand(self, func, finalBind=True):
        get_query = self.__getCommand_helper(func, finalBind)

        if get_query:
            if func:
                #func = self.status['get_cmd_func']
                func(self.formatQuery(get_query))
            else:
                return get_query

    def formatQuery(self, query):  #Formats the input query and returns it
        query = query.lower()
        d_query = query.split(' ')

        if d_query[0] == self.info['name'].lower() and len(d_query) > 1:
            d_query.pop(0)
        try:
            for n in range(len(d_query)):
                if d_query[n] == '' or d_query[n] == ' ':
                    d_query.remove(n)
                elif d_query[n] == 'true':
                    d_query[n] = 'True'
                elif d_query[n] == 'false':
                    d_query[n] = 'False'
        except:
            pass

        if not self.info['number lock']:
            indexes = []
            for n in range(len(d_query)):
                if d_query[n] in self.WORD_TO_NUM.keys():
                    d_query[n] = self.WORD_TO_NUM[d_query[n]]
                    indexes.append(n)
            for i in range(len(indexes) - 1):
                if (indexes[0] + 1) != indexes[1]:
                    indexes.pop(0)
                else:
                    d_query[indexes[0]] = d_query[indexes[0]] + d_query[indexes[1]]
                    d_query.pop(indexes.pop(1))
                    for x in range(1, len(indexes)):
                        indexes[x] -= 1

        if not self.info['symbol lock']:
            for n in range(len(d_query)):
                if d_query[n] in self.WORD_TO_SYM.keys():
                    d_query[n] = self.WORD_TO_SYM[d_query[n]]

        return_query = ' '.join(d_query)
        return return_query

    #---------------------------------Mains-----------------------------------

    def start_main(self):
        self.start_interface()

        self.emptyStatus()
        self.update()
        
        self.status['run'] = True
        
        #self.wishMe()
        
        while self.status['run']:
            try:
                if self.info['mode'] == 'audio':
                    if self.info['recognition'] == 'online1':
                        query = self.takeCommand_Online1() #org>>>formatQuery
                        self.update()
                        self.processQuery(query)

                    elif self.info['recognition'] == 'offline1':
                        try:
                            self.refresh_Offline1()
                        except:
                            self.init_Offline1()
                        self.printStatus('Listening to VOICE...')
                        self.runMain_Offline1()

                    elif self.info['recognition'] == 'offline2':
                        query = self.takeCommand_Offline2()
                        self.update()
                        self.processQuery(query)
                    
                self.update()
            
            except:
                self.printException()
            
        self.close_interface()
        #self.remember()



if __name__ == '__main__':
    b = Base()
    b.remember()
