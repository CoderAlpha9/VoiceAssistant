from mesh import *

'''
elif "camera" in statement or "take a photo" in statement:
    ec.capture(0,"robo camera","img.jpg")
'''

class Main(Mesh):
    def processQuery(self, org_query, printUserSpeech=True): #Perfoms tasks according to input
        if org_query == '':
            return
            
        query = self.formatQuery(org_query)

        if printUserSpeech:
            self.printOnConsole(query)

        #org_d_query = self.get_dissected_query(org_query)
        d_query = self.get_dissected_query(query)

        if self.info['keyboard type'] and (d_query[0] != 'change')\
         and (d_query[0] != 'switch') and (d_query[0] != 'click'):
            pag.typewrite(" ".join(d_query) + " ")
            return

        elif self.info['mimic'] and (d_query[0] != 'mimic'):
            self.speak(query)
            return
        
        try:
            if 'wiki' in d_query[0]:
                self.wikiQuery(d_query, query)

            elif d_query[0] == 'open':
                try:
                    query = query[5:]
                except:
                    query = query[3:]
                self.open_app(self.splitDQuery(d_query, 1), query)

            elif d_query[0] == 'close' and \
                (self.searchDQuery(d_query, 1, 'that') or self.searchDQuery(d_query, 1, 'app')):
                self.agree()
                pag.click(1887, 16)

            elif d_query[0] == 'minimise' and \
                (self.searchDQuery(d_query, 1, 'that') or self.searchDQuery(d_query, 1, 'app')):
                self.agree()
                pag.click(1745, 20)

            elif d_query[0] == 'google' or d_query[0] == 'search':
                d_query = self.splitDQuery(d_query, 1)
                self.agree()
                url = "https://www.google.com/search?q=" + '+'.join(d_query)
                self.webOpen(url)

            elif 'web' in d_query:
                self.agree()
                self.search_web(query.replace('web', ''))

            elif 'youtube' in d_query:
                d_query = self.splitDQuery(d_query, 1)
                self.agree()
                url = "https://www.youtube.com/results?search_query=" + '+'.join(d_query)
                self.webOpen(url)

            elif d_query[0] == 'home' and self.searchDQuery(d_query, 1, 'search'):
                self.agree()
                pag.click(186, 1055)
                time.sleep(0.5)
                pag.typewrite(' '.join(self.splitDQuery(d_query, 2)))

            elif (d_query[0] == 'app' or d_query[0] == 'screen') and \
                self.searchDQuery(d_query, 1, 'search'):
                self.agree()
                pag.typewrite(['f3'])
                time.sleep(0.5)
                pag.typewrite(' '.join(self.splitDQuery(d_query, 2)))

            elif d_query[0] == 'say':
                self.sayQuery(d_query, query)

            elif d_query[0] == 'show':
                self.showObj(d_query, query)

            elif d_query[0] == 'mimic':
                self.info['mimic'] = not self.info['mimic']
                if self.info['mimic']:
                    self.speak(f'Mimicking you {self.info["master"]}!')
                else:
                    self.speak(f'Stopped mimicking you {self.info["master"]}!')

            elif d_query[0] == 'write' or d_query[0] == 'type':
                time.sleep(1.25)
                #pag.click(pag.position())
                pag.typewrite(' '.join(self.splitDQuery(d_query, 1)))

            elif d_query[0] == 'click':
                if len(d_query) == 1:
                    pag.click(pag.position())
                else:
                    try:
                        pag.typewrite([org_query[6:]])
                    except:
                        self.speak('The requested key was not executable. Please try again!')
            
            elif self.inQuery('change background',query) or \
                self.inQuery('change desktop',query):
                self.agree()
                src = self.dirs['pics']
                src = os.path.join(src, random.choice(os.listdir(src)))
                ctypes.windll.user32.SystemParametersInfoW(20, 0, src, 0)
                self.speak("Desktop background changed successfully!")

            elif self.inQuery('change brightness to',query):
                query = query.replace("change brightness to ","")
                brightness = query 
                c = wmi.WMI(namespace='wmi')
                methods = c.WmiMonitorBrightnessMethods()[0]
                methods.WmiSetBrightness(brightness, 0)

            elif self.inQuery('change volume to',query):
                devices = AudioUtilities.GetSpeakers()
                device_interfacer = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = ctypes.cast(device_interfacer, ctypes.POINTER(IAudioEndpointVolume))
                
                query = int(query.replace("change volume to ",""))
                #-65(0) to 0(100)
                volume.SetMasterVolumeLevel(query, None)
                #subprocess.call(["amixer", "-D", "pulse", "sset", "Master", f"{query}%"])
                #subprocess.call(["osascript -e 'set volume output volume 100'"], shell=True)

            elif d_query[0] == 'switch' or d_query[0] == 'change':
                self.changeObj(d_query, query)

            elif self.inQuery("where is",query):
                location = query.replace("where is ", "")
                self.speak("Locating " + location + '...')
                self.webOpen("https://www.google.com/maps/place/" + location)

            elif 'exit' in d_query or 'quit' in d_query or 'bye' in d_query:
                self.execProtocol('exit')

            elif 'stop' in d_query and 'speech' in d_query:
                self.ENGINE.stop()

            elif 'cd' in d_query:
                indx = d_query.index('cd') + 1
                directory = d_query[indx:indx+1]
                
                try:
                    if directory[2:3] != ':':
                        directory = os.path.join(os.getcwd(), directory)
                except:
                    directory = os.path.join(os.getcwd(), directory)
                    
                self.info['current directory'] = directory

            elif self.inQuery("view note",query) or \
                self.inQuery('read note',query):
                
                def binder(filename):
                    with open(f'{self.dirs["output"]}/{filename}.txt', "r") as file:
                        self.speak(file.read())
                        
                self.speak("Input file name")
                self.getCommand(binder)

            elif "note" in d_query:
                self.setNote()

            elif self.inQuery('add todo',query):
                self.agree()
                todo_work = ' '.join(self.splitDQuery(d_query, 2))
                self.todo.append(todo_work)
                todo_str = ''
                for workNo in range(len(self.todo)):
                    todo_str += str(workNo + 1) + '. ' + self.todo[workNo] + '\n'
                self.printSpeech(todo_str)

            elif self.inQuery('remove todo',query) or \
                self.inQuery('delete todo',query):

                self.remTodo(d_query, query)

            elif 'todo' in d_query:
                todo_str = ''
                for workNo in range(len(self.todo)):
                    todo_str += str(workNo + 1) + '. ' + self.todo[workNo] + '\n'
                if todo_str == '':
                    self.speak('There are currently no todoes!')
                    return
                self.speak('Getting your todo list...')
                self.printSpeech(todo_str)

            elif self.inQuery('transfer control to',query):
                d_query = self.get_dissected_query(org_query)
                index = d_query.index('to')
                self.info["master"] = ' '.join(d_query[index+1:])
                self.userHead.configure(text = self.info['master'].upper())
                self.speak('Transferred assistant control to ' + self.info['master'] + '...')
                self.wishMe()

            elif d_query[0] == 'flip':
                if self.info['mode'] == 'audio':
                    self.info['mode'] = 'text'
                    self.speak('Switched input mode to text...')
                else:
                    self.info['mode'] = 'audio'
                    self.speak('Switched input mode to audio...')

            elif d_query[0] == 'toss':
                self.info['say'] = not self.info['say']
                self.speak(f'Changed say to {self.info["say"]}')

            elif d_query[0] == 'execute' or d_query[0] == 'exec':
                self.agree()
                d_query = org_query.split(' ')
                exec(' '.join(self.splitDQuery(d_query, 1)))

            elif d_query[0] == 'command' or d_query[0] == 'cmd':
                self.agree()
                d_query = org_query.split(' ')
                subprocess.call(' '.join(self.splitDQuery(d_query, 1)), shell=False)
                    
            elif self.inQuery('mail to me',query):
                self.sendMailToMe()

            elif self.inQuery('send a mail',query):
                self.sendMail()

            elif self.inQuery('find file',query):
                self.findFile(d_query, query)

            elif self.inQuery('organize files',query):
                self.organiseFiles()

            elif 'read' in d_query:
                self.ENGINE.setProperty('rate', self.info['read rate'])
                if self.info['mode'] == 'audio':
                    pag.hotkey('ctrl', 'c')
                time.sleep(0.05)
                self.speak(self.getClipData())
                self.ENGINE.setProperty('rate', self.info['speak rate'])

            elif 'music' in d_query or 'song' in d_query:
                songs = os.listdir(self.dirs['songs'])
                self.agree()
                os.startfile(os.path.join(self.dirs['songs'], songs[random.choice(self.searchList(songs, 'iron'))]))

            elif 'calc' in d_query:
                query = ''.join(self.splitDQuery(d_query, 1))
                if query == '':
                    self.speak('Enter a valid input!')
                else:
                    self.speak(f'The answer is: {eval(query)}.')

            elif 'time' in d_query:
                strTime = datetime.datetime.now().strftime('%H:%M')
                self.speak(f'{self.info["master"]} the time is {strTime}.')

            elif 'yesterday' in d_query or \
                (('last' in d_query or 'previous' in d_query) and 'day' in d_query):
                day, date, month, year = self.getDate('yesterday')
                self.speak(f'{self.info["master"]} yesterday was {day}, The {date} of {month}, {year}.')

            elif 'tomorrow' in d_query or ('next' in d_query and 'day' in d_query):
                day, date, month, year = self.getDate('tomorrow')
                self.speak(f'{self.info["master"]} tomorrow is {day}, The {date} of {month}, {year}.')

            elif 'day' in d_query or 'date' in d_query or 'today' in d_query:
                day, date, month, year = self.getDate()
                self.speak(f'{self.info["master"]} today is {day}, The {date} of {month}, {year}.')

            elif 'last' in d_query or 'previous' in d_query:
                if 'month' in d_query:
                    month = datetime.datetime.now().month - 1
                    year = datetime.datetime.now().year
                    
                    if month == 0:
                        month = 12
                        year -= 1

                    month = self.MONTHS[month]
                    self.speak(f'{self.info["master"]} last month was {month}, {year}.')
                    
                elif 'year' in d_query:
                    self.speak(f'{self.info["master"]} last year was {datetime.datetime.now().year - 1}.')

            elif 'next' in d_query:
                if 'month' in d_query:
                    month = datetime.datetime.now().month + 1
                    year = datetime.datetime.now().year
                    
                    if month == 13:
                        month = 1
                        year += 1

                    month = self.MONTHS[month]
                    self.speak(f'{self.info["master"]} next month is {month}, {year}.')
                
                elif 'year' in d_query:
                    self.speak(f'{self.info["master"]} next year is {datetime.datetime.now().year + 1}.')

            elif 'month' in d_query:
                self.speak(f'{self.info["master"]} the month is {datetime.datetime.now().month}.')

            elif 'year' in d_query:
                self.speak(f'{self.info["master"]} the year is {datetime.datetime.now().year}.')
                
            elif 'now' in d_query:
                strTime = datetime.datetime.now().strftime('%H:%M')
                day, date, month, year = self.getDate()
                self.speak(f'{self.info["master"]} the time is {strTime}' +
                    f' and today is {day}, The {date} of {month}, {year}.')

            elif 'alarm' in d_query:
                self.setAlarm()

            elif 'record' in d_query:
                if 'audio' in d_query or 'voice' in d_query:
                    
                    def binder(filename):
                        self.recordVoice(filename)
                    
                    self.speak('Input File Name')
                    self.getCommand(binder)

            elif 'play' in d_query:
                if 'recording' in d_query or 'audio' in d_query or 'voice' in d_query:

                    def binder(filename):
                        self.speak(f'Playing audio file: {filename}.mp3')
                        os.startfile(f"{self.dirs['output']}/{filename}.mp3")
                    
                    self.speak('Input File Name')
                    self.getCommand(binder)

            elif "camera" in d_query or "photo" in d_query:

                def binder(filename):
                    ec.capture(0, "Jarvis Camera", filename)
                
                self.speak('Input File Name')
                self.getCommand(binder)

            elif 'joke' in d_query:
                self.speak(pyjokes.get_joke())

            elif self.inQuery("countdown of",query):
                query = int(query.replace("countdown of ",""))
                listOfNum = []
                for i in range(query):
                    listOfNum.append(i)
                for i in range(query):
                    print(listOfNum.pop())

            elif self.inQuery("don't listen",query) or \
                self.inQuery("stop listening",query):

                def binder(t):
                    self.speak('Sleeping for: ' + t + ' seconds...')
                    time.sleep(int(t))
                
                self.speak("Enter sleeping time")
                self.getCommand(binder)

            elif self.inQuery('lock window',query):
                self.speak("Locking the device...")
                self.execProtocol('exit')
                ctypes.windll.user32.LockWorkStation()

            elif 'shutdown' in d_query or \
                ('shut' in d_query and 'down' in d_query):

                def binder(a):
                    if 'yes' in a or 'yeah' in a or 'definitely' in a:
                        self.speak("Shutting the system down...")
                        self.execProtocol('exit')
                        subprocess.call('shutdown /p /f')
                    else:
                        self.speak('That was close!')
                        return
                
                self.speak('Are you sure to shutdown the system ' + self.info['master'] + '?')
                self.getCommand(binder)

            elif "restart" in d_query:

                def binder(a):
                    if 'yes' in a or 'yeah' in a or 'definitely' in a:
                        self.speak("Restarting the system...")
                        self.execProtocol('exit')
                        subprocess.call(["shutdown", "/r"])
                    else:
                        self.speak('That was close!')
                        return
                
                self.speak('Are you sure to restart the system ' + self.info['master'] + '?')
                self.getCommand(binder)

            elif "hibernate" in d_query:

                def binder(a):
                    if 'yes' in a or 'yeah' in a or 'definitely' in a:
                        self.speak("Hibernating...")
                        self.execProtocol('exit')
                        subprocess.call("shutdown /h")
                    else:
                        self.speak('That was close!')
                        return
                
                self.speak('Are you sure to make the system hibernate ' + self.info['master'] + '?')
                self.getCommand(binder)

            elif self.inQuery("log off",query) or \
                self.inQuery("sign out",query):
                self.speak("Signing out...")
                self.execProtocol('exit')
                subprocess.call(["shutdown", "/l"])

            elif self.inQuery('recycle bin',query):
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                self.speak("Cleared Recycle bin...")

            elif 'screenshot' in d_query:
                pic = pag.screenshot()
            
                self.speak('Input File Name...')
                self.getCommand(lambda filename: pic.save(filename))

            elif self.inQuery('random number',query):
                self.speak(str(random.randint(1,100)))

            elif 'quote' in d_query:
                self.speak('The quote of the day is: ' + wikiquote.quote_of_the_day())

            elif 'thank' in d_query:
                self.speak(random.choice(('My Pleasure ', ' Pleasure ', 'You are welcome ', 'Welcome ')) + self.info['master'])

            elif 'hi' in d_query or 'hello' in d_query or 'hey' in d_query:
                self.speak(f'{random.choice(("Hello", "Hi", "Hey"))} {self.info["master"]}!')

            elif 'fine' in d_query or "good" in d_query:
                self.speak("It's good to know that you are fine")

            elif ('how' in d_query and 'old' in d_query and 'you' in d_query) \
                or ('your' in d_query and 'age' in d_query):
                self.sayAge()

            elif self.inQuery('how are you',query):
                self.speak("I am fine, Thank you... How are you " + self.info['master'] + '?')

            elif 'what' in d_query and 'your' in d_query and 'name' in d_query:
                self.speak("My name is " + self.info['name'].upper() + ' ' + self.info['master'] + '...')

            elif ('what' in d_query or 'whats' in d_query or "what's" in d_query)\
                 and 'up' in d_query:
                self.speak('My systems are looking good, thank you...')

            elif self.inQuery("who made you",query) or \
                self.inQuery("who created you",query):
                self.speak(f"I have been created by Jaiwanth Karthi {self.info['master']}...")

            elif "who" in d_query and 'you' in d_query:
                self.speak("I am your virtual assistant, " + self.info['name'].upper() + '...')

            elif "what" in d_query and "version" in d_query:
                self.speak(f"My version is {self.info['version']}.")

            elif "who" in d_query and 'i' in d_query:
                self.speak(f"You are my master {self.info['master']}!")

            elif self.inQuery("why did you come",query):
                self.speak("Thanks to Jaiwanth Karthi. Furthermore, It's a secret!")

            elif self.inQuery('is love',query):
                self.speak("It is 7th sense that destroy all other senses")

            elif self.inQuery("i love you",query):
                self.speak("It's hard to understand")

            elif self.inQuery('reason for you',query):
                self.speak("I was created as a python project by Jaiwanth Karthi")

            elif "calculate" in d_query:
                app_id = self.api_keys['wolframalpha']
                client = wolframalpha.Client(app_id)
                index = d_query.index('calculate')
                query = d_query[index + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                self.speak("The answer is " + answer)

            elif self.inQuery("what is",query) or \
                self.inQuery("who is",query):
                client = wolframalpha.Client(self.api_keys['wolframalpha'])
                res = client.query(query)
                try:
                    self.speak(next(res.results).text)
                except StopIteration:
                    self.speak("No results")

            elif self.inQuery("send message",query): 
                self.twilioMessage() 

            elif self.inQuery("send a whatsapp message",query):
                self.sendWhatsapp()

            elif "weather" in d_query:
                self.getWeather()

            elif self.inQuery('google news',query):
                self.getGoogleNews()

            elif self.inQuery("bbc news",query):
                self.getBbcNews()

            elif 'news' in d_query:
                self.getNews()

            elif 'pause' in d_query:
                input('Click "Enter" to continue...')
                
            elif 'favor' in d_query:
                self.agree()

            elif d_query[0] == self.info['name'].lower():
                self.speak(f'Yes {self.info["master"]}?')

            else:
                self.unindentifiedCommand(d_query, query)

        except:
            self.printException()
            self.emptyStatus()


#Statement to run the whole program
if __name__ == '__main__':
    m = Main()
    m.start_main()
