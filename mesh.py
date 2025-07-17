from interface import *


class Mesh(Interface):
        #---------------------------super helpers------------------

    def sendEmail(self, to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        #Enable low security in gmail
        server.login(self.info['email'], self.info['pass'])
        server.sendmail(self.info['email'], to, content)
        server.close()

    def __openInWeb(self, query):
        multiprocessing.Process(target=self.__openInWeb, args=(query,)).start()

    def webOpen(self, query):
        webbrowser.get(self.dirs['chrome']).open_new_tab(query)

    def search_web(self, indat):  #Searches the web for the given input-data
        self.printStatus(f'Opening browser to search for {indat}...')

        if 'youtube' in indat:
            self.speak("Opening in youtube")
            indx = indat.split().index('youtube')
            wordToSearch = indat.split()[indx + 1:]
            self.agree()
            self.webOpen("https://www.youtube.com/results?search_query =" + '+'.join(wordToSearch))

        elif 'wikipedia' in indat:
            self.speak("Opening Wikipedia")
            indx = indat.split().index('wikipedia')
            wordToSearch = indat.split()[indx + 1:]
            self.agree()
            self.webOpen("https://en.wikipedia.org/wiki/" + '_'.join(wordToSearch))

        elif 'google' in indat:
            indx = indat.split().index('google')
            wordToSearch = indat.split()[indx + 1:]
            self.agree()
            self.webOpen("https://www.google.com/search?q=" + '+'.join(wordToSearch))

        elif 'search' in indat:
            indx = indat.split().index('search')
            wordToSearch = indat.split()[indx + 1:]
            self.agree()
            self.webOpen("https://www.google.com/search?q=" + '+'.join(wordToSearch))

        else:
            self.webOpen("https://www.google.com/search?q=" + '+'.join(indat.split()))

        self.emptyStatus()

    def open_app(self, d_query, query):
        if 'youtube' in d_query:
            #self.webOpen('youtube.com')
            self.speak('Opening youtube')
            self.webOpen('https://www.youtube.com')

        elif 'wiki' in d_query:
            self.speak('Opening wikipedia')
            self.webOpen("https://www.wikipedia.com")

        #elif 'yahoo mail' in d_query:
        #   self.speak('Opening yahoo mail')
        #   self.webOpen('https://in.mail.yahoo.com')

        elif "mail" in d_query:
            self.speak('Opening google mail')
            self.webOpen('https://mail.google.com/mail/u/0/#inbox')

        elif 'classroom' in d_query:
            self.speak('Opening google classroom')
            self.webOpen('https://classroom.google.com/u/1/h')

        elif self.inQuery('stack overflow', query) or 'stackoverflow' in d_query:
            self.speak('Opening stack overflow')
            self.webOpen("stackoverflow.com")

        elif "chrome" in d_query:
            self.speak("Opening Chrome")
            os.startfile(self.dirs['google'])

        elif "google" in d_query:
            self.speak('Opening Google')
            self.webOpen('https://www.google.com')

        elif 'command' in d_query or 'cmd' in d_query:
            self.speak('Opening Command Prompt')
            os.startfile(self.dirs['cmd'])

        elif 'library' in d_query or 'files' in d_query:
            self.speak('Opening File Explorer')
            pag.click(261, 1057)
            pag.typewrite('file explorer')
            pag.typewrite(['enter'])

        elif 'settings' in d_query:
            self.speak('Opening Settings')
            pag.click(261, 1057)
            pag.typewrite('settings')
            pag.typewrite(['enter'])

        elif self.inQuery('voice recorder', query) or \
                self.inQuery('sound recorder', query):
            self.speak('Opening Voice Recorder')
            pag.click(261, 1057)
            pag.typewrite('voice recorder')
            pag.typewrite(['enter'])

        elif 'photo' in d_query or 'photos' in d_query or 'gallery' in d_query:
            self.speak('Opening Photos')
            pag.click(261, 1057)
            pag.typewrite('photos')
            pag.typewrite(['enter'])

        elif 'camera' in d_query:
            self.speak('Opening Camera')
            pag.click(261, 1057)
            pag.typewrite('camera')
            pag.typewrite(['enter'])

        elif "power" in d_query or "presentation" in d_query:
            self.speak("Opening Powerpoint")
            os.startfile(self.dirs['powerpoint'])

        elif "word" in d_query:
            self.speak("Opening Word")
            os.startfile(self.dirs['word'])

        elif "excel" in d_query:
            self.speak("Opening Excel")
            os.startfile(self.dirs['excel'])

        elif 'control' in d_query:
            self.speak("Opening Control Panel")
            os.startfile(self.dirs['control panel'])

        elif ('task' in d_query and 'manager' in d_query):
            self.speak("Opening Task Manager")
            os.startfile(self.dirs['task_manager'])

        elif 'code' in d_query:
            self.speak('Opening Visual Studio Code')
            os.startfile(self.dirs['vs_code'])

        elif 'python' in d_query or 'idle' in d_query:
            self.speak('Opening Python IDLE')
            os.startfile(self.dirs['python'])

        elif 'pycharm' in d_query:
            self.speak('Opening PyCharm')
            os.startfile(self.dirs['pycharm'])

        else:
            try:
                if 'cube' in d_query:
                    multiprocessing.Process(target=vCube).start()
                    self.speak('Opening Virtual Cube Simulater')
                elif 'calc' in query or 'hexon' in d_query:
                    multiprocessing.Process(target=run_hexon).start()
                    self.speak('Opening Calculater Hexon')
                elif 'clock' in d_query:
                    multiprocessing.Process(target=run_clock).start()
                    self.speak('Opening clock')
                else:
                    raise Exception

            except:
                self.speak('Sorry, the program was not identifiable. Please try again!')

    #---------------------------helper processes--------------------------------------

    def wikiQuery(self, d_query, query):
        query = ' '.join(self.splitDQuery(d_query, 1))
        self.ENGINE.setProperty('rate', self.info['read rate'])
        try:
            try:
                with open(f'{self.dirs["dependencies"]}/text_dependencies/Wikipedia/{query[0].upper()}.txt', 'r') as file:
                    data = eval(file.read())
                self.speak('According to cached wikipedia data, ' + data[f'{query}'])

            except FileNotFoundError:
                #self.printStatus('Searching Wikipedia...')
                results = wikipedia.summary(query, sentences=self.info['wikipedia sentences'])
                #self.printStatus('Creating wiki-log...')
                with open(f'{self.dirs["dependencies"]}/text_dependencies/Wikipedia/{query[0].upper()}.txt', 'w') as file:
                    data = {f'{query}': results}
                    file.write(f'{data}')

                self.speak('According to wikipedia, ' + results)

            except KeyError:
                #self.printStatus('Searching Wikipedia...')
                results = wikipedia.summary(query, sentences=self.info['wikipedia sentences'])
                #self.printStatus('Writing wiki-info to existing logs...')
                with open(f'{self.dirs["dependencies"]}/text_dependencies/Wikipedia/{query[0].upper()}.txt', 'r') as file:
                    data = eval(file.read())
                with open(f'{self.dirs["dependencies"]}/text_dependencies/Wikipedia/{query[0].upper()}.txt', 'w') as file:
                    data[f'{query}'] = results
                    file.write(f'{data}')

                self.speak('According to wikipedia, ' + results)

        except:
            self.speak(f'Sorry, No page related to the given query was found {self.info["master"]}...')

        self.ENGINE.setProperty('rate', self.info['speak rate'])

    def sayQuery(self, d_query, query):
        try:
            if (self.searchDQuery(d_query, 1, 'hi') or self.searchDQuery(d_query, 1, 'hello')\
                or self.searchDQuery(d_query, 1, 'hey')) and ('to' in d_query):
                try:
                    d_query.remove('to')
                    try:
                        d_query.remove('my')
                    except:
                        pass

                    self.speak(random.choice(('Hi ', 'Hello ')) + \
                        ' '.join(self.splitDQuery(d_query, 2)) + '!')
                except:
                    query = query[4:]
                    self.speak(query)
            else:
                query = query[4:]
                self.speak(query)
        except:
            pass

    def showObj(self, d_query, query):
        nxt = self.splitDQuery(d_query, 1)
        if 'todos' in nxt or 'todoes' in nxt or 'to-does' in nxt:
            todo_str = 'Todos:\n'
            for workNo in range(len(self.todo)):
                todo_str += str(workNo + 1) + '. ' + self.todo[workNo] + '\n'
            if todo_str == 'Todos:\n':
                self.speak('There are currently no todoes!')
                return
            self.printSpeech(todo_str)

        elif 'alarm' in nxt or 'alarms' in nxt:
            rem_str = 'Alarms:\n'
            for rem in self.remainders.keys():
                current_rem = self.remainders[rem]
                rem_str += f'{rem} @ {current_rem[0]}:{current_rem[1]}\n'
            if rem_str == 'Alarms:\n':
                self.speak('There are currently no alarms!')
                return
            self.printSpeech(rem_str)

        else:
            q = query[5:]
            try:
                self.printSpeech(str(self.info[q]))
            except:
                try:
                    self.printSpeech(f"{q}:\n" + eval(f"str(self.{q})"))
                except:
                    self.speak('Object requested is not identifiable...')

    def changeObj(self, d_query, query):
        bpi = d_query.index('to')
        q1 = ''
        for n in range(1, bpi):
            q1 = q1 + d_query[n] + ' '
        q1 = q1[:len(q1) - 1]

        if q1 in self.info.keys():
            q2 = ''
            for n in range(bpi + 1, len(d_query)):
                q2 = q2 + d_query[n] + ' '
            q2 = q2[:len(q2) - 1]

            try:
                q2 = eval(q2)
            except:
                pass

            self.info[q1] = q2

            if q1 == 'voice':
                try:
                    self.ENGINE.setProperty('voice', self.VOICES[self.VOICE_DICT[self.info['voice']]].id)
                except Exception:
                    try:
                        self.ENGINE.setProperty('voice', self.VOICES[int(self.info['voice'])].id)
                    except Exception:
                        return

            elif q1 == 'name':
                self.win.title(f'{q2.upper()} v{self.info["version"]}')
                self.nameHead.configure(text = q2.upper())

            elif q1 == 'version':
                self.win.title(f'{self.info["name"].upper()} v{q2}')
            
            elif q1 == 'master':
                self.userHead.configure(text = q2.upper())

            elif q1 == 'speak rate':
                self.ENGINE.setProperty('rate', q2)
                
            self.speak(f'Changed {q1} to {q2}')
        
        else:
            self.speak("The object requested is unidentifiable. Please try again!")

    def remTodo(self, d_query, query):
        self.agree()
        todo_work = ' '.join(self.splitDQuery(d_query, 2))
        try:
            todo_work = int(todo_work)
            if 0 > todo_work > len(self.todo):
                self.todo.pop(todo_work - 1)
            else:
                self.speak("Can't remove todo as it doesn't exist...")
                return
        except:
            if todo_work in self.todo:
                self.todo.pop(self.todo.index(todo_work))
            else:
                self.speak("Can't remove todo work as it doesn't exist...")
                return
        todo_str = ''
        for workNo in range(len(self.todo)):
            todo_str += str(workNo + 1) + '. ' + self.todo[workNo] + '\n'
        if todo_str == '':
            self.speak('There are currently no todoes!')
            return
        self.printSpeech(todo_str)

    def findFile(self, d_query, query):
        find = query.replace('find file ', '') #File or folder to find
        caps_lock = self.info['file find'][0] #True if the name should be searched as it is
        open_it = self.info['file find'][1] #True if file or directory needs to be opened automatically
        partial_name = self.info['file find'][2] #False if name is to be searched without addition
        single_file = self.info['file find'][3] #False if many files of the same name are to be found

        if not caps_lock:
            find = find.lower()

        found = False
        text_str = ''
        
        list_of_files = os.walk(self.info["current directory"])

        for dirpath, dirnames, filenames in list_of_files:

            if not caps_lock:
                for fileNo in range(len(filenames)):
                    filenames[fileNo] = filenames[fileNo].lower()

                for dirNo in range(len(dirnames)):
                    dirnames[dirNo] = dirnames[dirNo].lower()

            if not partial_name:
                if find in filenames:
                    file_p = os.path.join(dirpath, find)
                    text_str += ' -Found match! : ' + str(file_p)
                    found = True
                    
                    if open_it:
                        os.startfile(file_p)
                    if single_file:
                        break

                elif find in dirnames:
                    dir_p = os.path.join(dirpath, find)
                    text_str += ' -Found match! : ' + str(dir_p)
                    found = True
                    
                    if open_it:
                        os.startfile(dir_p)
                    if single_file:
                        break
            else:
                if (find in filename for filename in filenames):
                    file_p = os.path.join(dirpath, find)
                    text_str += ' -Found match! : ' + str(file_p)
                    found = True
                    
                    if open_it:
                        os.startfile(file_p)
                    if single_file:
                        break

                elif (find in dirname for dirname in dirnames):
                    dir_p = os.path.join(dirpath, find)
                    text_str += ' -Found match! : ' + str(dir_p)
                    found = True
                    
                    if open_it:
                        os.startfile(dir_p)
                    if single_file:
                        break

        if not found:
            self.speak('No file detected...')
        else:
            self.speak('File detected!')
            self.printSpeech(text_str)

    def organiseFiles(self):
        for entry in os.scandir():
            if entry.is_dir():
                continue
            file_path = Path(entry.name)
            file_format = file_path.suffix.lower()
            if file_format in self.FILE_FORMATS:
                directory_path = Path(self.FILE_FORMATS[file_format])
                directory_path.mkdir(exist_ok=True)
                file_path.rename(directory_path.joinpath(file_path))
        try:
            os.mkdir("OTHER")
        except:
            pass
        for dir in os.scandir():
            try:
                if dir.is_dir():
                    os.rmdir(dir)
                else:
                    os.rename(self.info["current directory"] + '/' + str(Path(dir)), self.info["current directory"] + '/OTHER/' + str(Path(dir)))
            except:
                pass
    
    def setNote(self):
        def binder(filename):
            def binder_1(note):
                with open(f'{self.dirs["output"]}/{filename}.txt', 'w') as file:
                    file.write(note)
                self.speak('Note written...')
            
            self.speak(f"What should i write {self.info['master']}?")
            #self.status['get_cmd_queue'].append(binder_1)
            self.getCommand(binder_1)
        
        self.speak('Input file name')
        self.getCommand(binder, False)

    def sendMailToMe(self):
        try:
            def binder(content):
                self.sendEmail(self.info['email'], content)
                self.speak("Email has been sent !")
                
            self.speak("What should I say?")
            self.getCommand(binder)
            
        except Exception:
            self.speak("I was not able to send this email")
            self.printException()         
    
    def sendMail(self):
        try:
            def binder(content):
                def binder_1(to):
                    self.sendEmail(to, content)
                    self.speak("Email has been sent !")
                
                self.speak("Whom should i send to?")
                #tempInfoMode = self.info['mode']
                #self.info['mode'] = 'text'
                #self.status['get_cmd_queue'].append(binder_1)
                self.getCommand(binder_1)
                #self.info['mode'] = tempInfoMode

            self.speak("What should I say?")
            self.getCommand(binder, False)
            
        except Exception:
            self.speak("I was not able to send this email")
            self.printException()

    def setAlarm(self):
        def binder(hour):
            def binder_1(minute):
                def binder_2(rem):
                    self.remainders[rem] = (hour, minute)
                    self.agree()
                
                self.speak('Input Remainder')
                #self.status['get_cmd_queue'].append(binder_2)
                self.getCommand(binder_2)
            
            self.speak('Input Minute')
            #self.status['get_cmd_queue'].append(binder_1)
            self.getCommand(binder_1, False)
        
        self.speak('Input Hour')
        self.getCommand(binder, False)

    def sayAge(self):
        dif = datetime.datetime.now() - self.CREATED
        months = int(dif.days/30.4375)
        years = int(months/12)
        
        m_ending = 'months' if months>1 else 'month'
        y_ending = 'years' if years>1 else 'year'

        if years == 0:
            self.speak(f"I am {months} {m_ending} old {self.info['master']}!")
        else:
            if months%12 == 0:
                self.speak(f"I am {years} {y_ending} old {self.info['master']}!")
            else:
                self.speak(f"I am {years} {y_ending} and {months} {m_ending} old {self.info['master']}!")

    def twilioMessage(self):
        # You need to an account on Twilio to use this
        account_sid = self.api_keys['twilio'][0]
        auth_token = self.api_keys['twilio'][1]
        client = Client(account_sid, auth_token)
        self.speak('Input message')

        def binder(ans):
            message = client.messages.create(body = ans, \
                from_=self.info['twilio_send_no'], to =self.info['twilio_rec_no'])
            self.speak('Messaged : ')
            self.printSpeech(message.sid)
        
        self.getCommand(binder)

    def sendWhatsapp(self):
        return
        '''
        def binder(name):

            def binder_1(msg):
                count = 1
                user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
                user.click()
                msg_box = driver.find_element_by_class_name('_3u328')
                for i in range(count):
                    msg_box.send_keys(msg)
                    button = driver.find_element_by_class_name('_3M-N-')
                    button.click()
        
            self.speak("Enter Your Message")
            #self.status['get_cmd_queue'].append(binder_1)
            self.getCommand(binder_1)

        driver = webdriver.Chrome(self.dirs['chrome'])
        driver.get('https://web.whatsapp.com/')
        self.speak("Scan QR code before proceding")
        tim = 10
        time.sleep(tim)
        self.speak("Enter Name of Group or User")
        self.getCommand(binder, False)
        '''
    
    def getWeather(self):
        # Google Open weather website 
        # to get API of Open weather  
        api_key = self.api_keys['openWeather']
        base_url = "https://api.openweathermap.org/data/2.5/weather?"

        def binder(city_name):
            complete_url = base_url + "appid =" + api_key + "&q =" + city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                self.speak(" Temperature (in kelvin unit) = " + str(
                    current_temperature) + " atmospheric pressure (in hPa unit) =" + str(
                    current_pressure) + " humidity (in percentage) = " + str(
                    current_humidity) + " description = " + str(weather_description))

            else:
                self.speak(" City Not Found ")
                    
        self.speak("Enter City name:")
        self.getCommand(binder)

    def getGoogleNews(self):
        jsonObj = urlopen("https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=self.api_keys['googleNews']")
        data = json.load(jsonObj)
        i = 1
        self.speak('')
        print("===============Google News============"+ "\n")
        for item in data['articles']:
            print(str(i) + '. ' + item['title'] + '\n')
            print(item['description'] + '\n')
            self.speak(str(i) + '. ' + item['title'] + '\n')
            i += 1

    def getBbcNews(self):
        main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=self.api_keys['bbc']"
        open_bbc_page = requests.get(main_url).json() 
        article = open_bbc_page["articles"] 
        results = [] 
        for ar in article: 
            results.append(ar["title"]) 
        for i in range(len(results)): 
            print(i + 1, results[i])

    def getNews(self):
        jsonObj = urlopen(f"https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=\\{self.api_keys['timesOfIndia']}\\")
        data = json.load(jsonObj)
        i = 1

        self.speak('here are some top news from the times of india')
        self.printSpeech('''from TIMES OF INDIA''')

        for item in data['articles']:
            self.printSpeech(str(i) + '. ' + item['title'])
            self.printSpeech(item['description'])
            self.speak(str(i) + '. ' + item['title'])
            i += 1

    def unindentifiedCommand(self, d_query, query):
        def binder(ans):
            if not ans:
                self.info['web search?'] = query
            elif 'yes' in ans or 'yeah' in ans or 'sure' in ans or 'definitely' in ans: 
                self.search_web(query)
            elif 'no' in ans or 'nope' in ans or 'never' in ans or 'dont' in ans:
                return
            else:
                self.processQuery(ans, False)
        
        if 'youtube' in d_query or 'wikipedia' in d_query or 'google' in d_query or 'search' in d_query:
            self.search_web(query)
            return

        #self.speak("I can search the web for you, Do you want to continue?")
        self.printSpeech('Unidentified Command....')
        self.getCommand(binder)


if __name__ == '__main__':
    Mesh()