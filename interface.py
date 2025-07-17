from base import *
#import tkinter as tk
#from PIL import ImageTk, Image


class Interface(Base, threading.Thread):
    #dirs = {'dependencies' : 'D:/Users/CoderAlpha/Documents/Prog/Python/py_proj/projectX'}
    #info = {'name': 'jarvis', 'master': 'Jaiwanth', 'version': '3.1'}

    nss_actions_options = ["Exec Code", "Speak", "Start File", \
        "Open in web", "Type", "Click"]

    #--------------------------------------Main interface---------------------------------------

    def start_interface(self):
        #threading.Thread.__init__(self)
        self.last_row = 1
        
        self.win = tk.Tk()
        self.icon = tk.PhotoImage(file = self.dirs['dependencies']+'/image_dependencies/main_logo.png')
        self.win.iconphoto(False, self.icon)
        self.win.title(f'{self.info["name"].upper()} v{self.info["version"]}')
        self.win.resizable(0, 0)
        
        #self.win.geometry(f'{self.geometry[0]}x{self.geometry[1]}+' +\
        #                    f'{self.geometry[2]}+{self.geometry[3]}')
        self.__connectMenu()

        #self.backgroundImage = Image.open(self.dirs['dependencies'] + '/image_dependencies/bg.jpg')
        #self.backgroundImage = self.backgroundImage.resize((self.geometry[0],self.geometry[1]))
        #self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)
        #self.backgroundFrame = tk.Label(self.win, image = self.backgroundImage, bg = 'black')
        ##self.backgroundFrame = resizablePicFrame(self.win, self.backgroundImage)
        #self.backgroundFrame.grid(rowspan = 9)

        self.mainFrm = tk.Frame(self.win, background='black')
        self.mainFrm.grid(column = 0, row = 0)

        self.statusLabel = tk.Label(self.mainFrm, bg='black', fg='#eaffea', font='Calibri 12 italic')
        self.statusLabel.grid(columnspan = 2)

        self.nameHead = tk.Label(self.mainFrm, text=self.info["name"].upper(), font='Calibri 14 bold', \
             width=25, wraplength='284', justify='left', bg='#300000', fg='#95caff')
        self.nameHead.grid(column=0, row=1)
        self.userHead = tk.Label(self.mainFrm, text=self.info["master"].upper(), font='Calibri 14 bold', \
            width=29, wraplength='289', justify='left', bg='#300000', fg='#95caff')
        self.userHead.grid(column=1, row=1)

        self.scrlFrm = tk.Frame(self.mainFrm) #background='red')
        self.scrlFrm.grid(column = 0, row = 2, columnspan = 2)
        #self.subScrlFrm = tk.Frame(self.scrlFrm, background='yellow')
        #self.subScrlFrm.pack(side='top') -> scrlCnvs & sby

        self.scrlCnvs = tk.Canvas(self.scrlFrm, background='black', \
            width=self.geometry[0]-20, height=self.geometry[1]-20)
        self.scrlCnvs.pack(side='left')
        self.inScrlFrm = tk.Frame(self.scrlCnvs, background='black')

        #self.sbx = tk.Scrollbar(self.scrlFrm, orient = "horizontal", command = self.scrlCnvs.xview)
        #self.sbx.pack(fill = "x", side='bottom')
        self.sby = tk.Scrollbar(self.scrlFrm, orient = "vertical", command = self.scrlCnvs.yview)
        self.sby.pack(fill = "y", side='right')
        #self.scrlCnvs.configure(xscrollcommand = self.sbx.set)
        self.scrlCnvs.configure(yscrollcommand = self.sby.set)

        self.scrlCnvs.create_window((0, 0), window = self.inScrlFrm)
        self.inScrlFrm.bind("<Configure>", \
            lambda event : self.scrlCnvs.configure(scrollregion=self.scrlCnvs.bbox("all")))
        #print(self.sby.get()))

        tk.Label(self.inScrlFrm, text=' '*30, bg='black', \
                 width=30).grid(column=0, row=0)
        tk.Label(self.inScrlFrm, text=' '*28, bg='black', \
                 width=28).grid(column=1, row=0)

        self.queryVar = tk.StringVar()
        self.queryEntry = tk.Entry(self.mainFrm, textvariable = self.queryVar, \
                                   width = 50, font = 'Calibri 13', fg='black')
        self.queryEntry.bind('<Return>', self.evalQuery)
        self.queryEntry.grid(column = 0, row = 3, columnspan = 2)

        self.win.protocol('WM_DELETE_WINDOW',self.__winClose)
        self.queryEntry.focus()

    def __helpFunc(self):
        print('Not Implemented...')

    def __aboutFunc(self):
        print(f'<Devoloped by Jaiwanth Karthi, {self.info["name"].upper()} v{self.info["version"]}>')

    def __connectMenu(self):
        menu = tk.Menu(self.win)

        helpmenu = tk.Menu(menu, tearoff = 0)
        helpmenu.add_command(label = 'Help...', command = self.__helpFunc, accelerator = 'Alt+H')
        helpmenu.add_command(label = 'About...', command = self.__aboutFunc, accelerator = 'Alt+A')
        menu.add_cascade(label = 'Help', menu = helpmenu)

        changemenu = tk.Menu(menu, tearoff = 0)
        changemenu.add_command(label = 'Set New Skill', command = self.start_nss, accelerator = 'Alt+N')
        #changemenu.add_command(label = 'About...', command = self.__aboutFunc, accelerator = 'Alt+A')
        menu.add_cascade(label = 'Change', menu = changemenu)

        self.win.config(menu=menu)

        self.win.bind("<Alt-h>", lambda e:self.__helpFunc())
        self.win.bind("<Alt-H>", lambda e:self.__helpFunc())
        self.win.bind("<Alt-a>", lambda e:self.__aboutFunc())
        self.win.bind("<Alt-A>", lambda e:self.__aboutFunc())

        self.win.bind("<Alt-n>", lambda e:self.start_nss())
        self.win.bind("<Alt-n>", lambda e:self.start_nss())

    def bindQueryEntry(self, key, func):
        self.queryEntry.bind(key, func)
        '''
        if func is self.evalQuery:
            self.status['get_cmd_func'] = self.processQuery
        else:
            self.status['get_cmd_func'] = func
        '''

    def evalQuery(self, event):
        return_query = (self.queryVar.get())
        self.queryVar.set('')
        #return_query = self.formatQuery(return_query)
        self.update()
        #self.printOnConsole(return_query)
        self.processQuery(return_query)
        self.update()

    def __winClose(self):
        self.execProtocol('exit')

    def close_interface(self):
        try:
            self.win.destroy()
        except:
            pass

#---------------------------New Skill Setter (NSS)------------------------------

    def start_nss(self):
        self.status['nss_open'] = True
        self.actions = []

        self.nss_console = tk.Tk()
        #self.nss_console = tk.Toplevel(self.win)

        self.nss_console.title('Set New Skill')

        self.nss_mainFrm = tk.Frame(self.nss_console, \
            background='black')
        self.nss_mainFrm.grid()

        tk.Label(self.nss_mainFrm, text='Enter new command: ', \
            bg='black', fg='white').grid()

        self.nss_cmdVar = tk.StringVar()
        self.nss_cmdEntry = tk.Entry(self.nss_mainFrm, textvariable=self.nss_cmdVar, width=35)
        self.nss_cmdEntry.grid(column=1, row=0, pady=20)

        tk.Button(self.nss_mainFrm, text='➕', \
            bg='black', fg='white').grid(column=2, row=0)
        #tk.Button(self.nss_mainFrm, text='➖', \
        #    bg='black', fg='white').grid(column=3, row=0)

        self.nss_slideFrm = tk.Frame(self.nss_mainFrm)
        self.nss_slideFrm.grid(column=0, row=1, columnspan=3)

        self.nss_scrlCnvs = tk.Canvas(self.nss_slideFrm, background='black', \
            width=self.nss_geometry[0]-20, height=self.nss_geometry[1]-20)
        self.nss_scrlCnvs.pack(side='left')
        self.nss_scrlFrm = tk.Frame(self.nss_scrlCnvs, background='black')
        
        self.nss_sby = tk.Scrollbar(self.nss_slideFrm, orient = "vertical", \
            command = self.nss_scrlCnvs.yview)
        self.nss_sby.pack(fill = "y", side='right')
        
        self.nss_scrlCnvs.configure(yscrollcommand = self.nss_sby.set)
        self.nss_scrlCnvs.create_window((0, 0), window = self.nss_scrlFrm)
        self.nss_scrlFrm.bind("<Configure>", \
            lambda event: self.nss_scrlCnvs.configure(scrollregion=self.nss_scrlCnvs.bbox("all")))

        tk.Label(self.nss_scrlFrm, bg='black').grid(padx=90)
        tk.Label(self.nss_scrlFrm, bg='black').grid(column=1, row=0, padx=170)

        self.nss_actionTypeFrm = tk.Frame(self.nss_scrlFrm, background='black')
        self.nss_actionTypeFrm.grid(column=0, row=1)
        self.nss_actionValueFrm = tk.Frame(self.nss_scrlFrm, background='black')
        self.nss_actionValueFrm.grid(column=1, row=1)

        self.__add_field()

        self.nss_btnFrm = tk.Frame(self.nss_mainFrm, background='black')
        self.nss_btnFrm.grid(columnspan=3)

        tk.Button(self.nss_btnFrm, text='del', bg='black', fg='white').grid(column=0, padx=75)
        tk.Button(self.nss_btnFrm, text='get', bg='black', fg='white').grid(column=1, row=0, padx=75, pady=15)
        tk.Button(self.nss_btnFrm, text='set', bg='black', fg='white').grid(column=2, row=0, padx=75)

        self.nss_console.protocol('WM_DELETE_WINDOW',self.__nss_close)
        self.nss_cmdEntry.focus()

    def __add_field(self):
        temp_var = tk.StringVar()
        temp_var.set(self.nss_actions_options[0])
        temp_drop = tk.OptionMenu(self.nss_actionTypeFrm, temp_var, *self.nss_actions_options)
        temp_drop.grid()
        #tk.Button(self.nss_actionTypeFrm, text='p', command=lambda:print(temp_var.get())).grid()

        temp_text = tk.Text(self.nss_actionValueFrm, width=33, height=7)
        temp_text.grid()
        
    def __nss_close(self):
        self.status['nss_open'] = False
        self.nss_console.destroy()

#----------------------------update aand mainloop-------------------------

    def __checkAlarm(self):
        hr = str(datetime.datetime.now().hour)
        mn = str(datetime.datetime.now().minute)
        for remainder in self.remainders.keys():
            if (self.remainders[remainder][0] == hr) and (self.remainders[remainder][1] == mn):
                self.speak(f'Remainder at {hr}:{mn}... {remainder}')
                del self.remainders[remainder]
                return

    def update_nss(self):
        if self.status['nss_open']:
            self.nss_console.update()

    def update(self, check_alarm=True):
        if check_alarm:
            self.__checkAlarm()
        try:
            self.win.update()
        except:
            pass
        
        self.update_nss()

    def mainloop(self):
        try:
            while self.status['run']:
                self.update()
        except:
            self.printException()
            print('Error in mainloop...')

#----------------------------console printing---------------------------

    def printOnConsole(self, text):
        try:
            tk.Label(self.inScrlFrm, text=text, width=25, wraplength='289', bg='black', font='Calibri 13', \
                    fg='#a4ffff', justify='left').grid(column=1, row=self.last_row)
        except:
            pass
        
        self.last_row += 1
        print(self.info['master'].upper() + ': ' + text)

    def printSpeech(self, text):
        text = ' '.join(text.split('\n'))

        try:
            tk.Label(self.inScrlFrm, text=text, width=27, wraplength='284', bg='black', font='Calibri 13', \
                    fg='#a4ffff', justify='left').grid(column=0, row=self.last_row)
        except:
            pass

        self.last_row += 1
        print(self.info['name'].upper() + ': ' + text)
        
    def printStatus(self, text):
        try:
            self.statusLabel.configure(text = text)
        except:
            pass
        #print(text)

    def emptyStatus(self):
        self.printStatus('Listening for input...')


if __name__ == '__main__':
    interface = Interface()
    interface.start_interface()
    interface.start_nss()
    while interface.status['run']:
        interface.update(False)
