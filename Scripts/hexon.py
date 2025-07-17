import tkinter as tk
from tkinter import TclError, _tkinter, messagebox, ttk, _test
import pickle as pkl
import math
    
#functions and classes
def RoundOff(num,place):
    try:
        num = str(num)
        place = int(place)
        nl = num.split('.')
        nl[1] = nl[1] + '0'
        fnl1t =int(nl[1][(place):(place+1)])
        fnl1u = nl[1][place-1:place]
        if fnl1t >= 5:
            fnl1u = str(int(fnl1u)+1)
        tnl1 = nl[1][0:(place-1)]
        fnl1 = tnl1+fnl1u
        return float(nl[0]+'.'+fnl1)
    except ValueError:
        Message('Input Error','Please choose a valid rounding measure.')

def Message(title,message,master = None):
    messagebox.showinfo(title,message)
    if master != None:
        master.focus()

def gcd(m,n):
    if m%n == 0:
        return n
    else:
        return gcd(n,m%n)

def ftf(num):
    ns = str(num)
    nl = ns.split('.')
    d = len(nl[1])
    den = 10**d
    n = int(str(nl[0]+str(nl[1])))
    return n,den

class Fraction():
    def __init__(self,numerator,denominator=1):
        if isinstance(numerator,float):
            numerator,a = ftf(numerator)
            denominator = denominator*a
        if isinstance(denominator,float):
            denominator,a = ftf(numerator)
            numerator = numerator*a
        g = gcd(numerator,denominator)
        self.numerator = numerator/g
        self.denominator = denominator/g

    def __str__(self):
        return '%d/%d' % (self.numerator,self.denominator)

    def __mul__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(self.numerator*other.numerator,self.denominator*other.denominator)
    
    __rmul__ = __mul__

    def __add__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(self.numerator*other.denominator + other.numerator*self.denominator , self.denominator*other.denominator)

    __radd__ = __add__

    def __sub__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(self.numerator*other.denominator - other.numerator*self.denominator , self.denominator*other.denominator)

    def __rsub__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(other.numerator*self.denominator - self.numerator*other.denominator , self.denominator*other.denominator)

    def __div__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(self.numerator*other.denominator,self.denominator*other.numerator)

    def __rdiv__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        return Fraction(other.numerator*self.denominator,other.denominator*self.numerator)

    def __neg__(self):
        return Fraction(0-(self.numerator),self.denominator)

    def __cmp__(self,other):
        if isinstance(other,int):
            other = Fraction(other)
        d1 = self.numerator/self.denominator
        d2 = other.numerator/other.denominator
        if d2 > d1:
            return False
        elif d2 == d1:
            return None
        else:
            return True

def mainAbout():
    messagebox.showinfo(title='About The Calculator Hexon',message="The Calculator Hexon v1.4 - 2020\nDevolped and Published by Jaiwanth Karthi\nCalculates values of all types!")
    root.focus()

def smClose(event):
    root.destroy()
    '''
    root.bell()
    mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Calulator Hexon?')
    if mg == True:
        root.destroy()
    else:
        pass
        root.focus()
    '''

def goto(w1,w2):
    def ex(event):
        w2.focus()
    def es(event):
        w1.focus()
    w1.bind('<Shift-Right>', ex)
    w2.bind('<Shift-Left>', es)

def gov(w1,w2):
    def ex(event):
        w2.focus()
    def es(event):
        w1.focus()
    w1.bind('<Return>', ex)
    w1.bind('<Shift-Down>', ex)
    w2.bind('<Shift-Up>', es)
    w1.bind('<Down>', ex)
    w2.bind('<Up>', es)

def shsa(w,sc):
    def ea(event):
        sc()
    w.bind('<Return>',ea)

class TooltipBase(object):
    
    def __init__(self, anchor_widget):
        self.anchor_widget = anchor_widget
        self.tipwindow = None

    def __del__(self):
        self.hidetip()

    def showtip(self):
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.anchor_widget)
        tw.wm_overrideredirect(1)
        try:
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w, "help", "noActivates")
        except:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  
        self.tipwindow.lift()

    def position_window(self):
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + x
        root_y = self.anchor_widget.winfo_rooty() + y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))

    def get_position(self):
        return 20, self.anchor_widget.winfo_height() + 1

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except:
                pass

class OnHoverTooltipBase(TooltipBase):

    def __init__(self, anchor_widget, hover_delay=0):
        super(OnHoverTooltipBase, self).__init__(anchor_widget)
        self.hover_delay = hover_delay

        self._after_id = None
        self._id1 = self.anchor_widget.bind("<Enter>", self._show_event)
        self._id2 = self.anchor_widget.bind("<Leave>", self._hide_event)
        self._id3 = self.anchor_widget.bind("<Button>", self._hide_event)

    def __del__(self):
        try:
            self.anchor_widget.unbind("<Enter>", self._id1)
            self.anchor_widget.unbind("<Leave>", self._id2)
            self.anchor_widget.unbind("<Button>", self._id3)
        except:
            super(OnHoverTooltipBase, self).hidetip()
            
    def _show_event(self, event=None):
        if self.hover_delay:
            self.schedule()
        else:
            self.showtip()

    def _hide_event(self, event=None):
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self._after_id = self.anchor_widget.after(self.hover_delay, self.showtip)

    def unschedule(self):
        after_id = self._after_id
        self._after_id = None
        if after_id:
            self.anchor_widget.after_cancel(after_id)

    def hidetip(self):
        try:
            self.unschedule()
        except TclError:
            pass
        super(OnHoverTooltipBase, self).hidetip()

class Hovertip(OnHoverTooltipBase):

    def __init__(self, anchor_widget, text, hover_delay=0):
        super(Hovertip, self).__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text

    def showcontents(self):
        label = tk.Button(self.tipwindow, text=self.text, background="#ffffff", borderwidth=1)
        label.pack()

def Arithmetic_calc_init():
    win = tk.Toplevel(root)
    menubar = tk.Menu(win)
    win.title('Arithmetic Progression Rule Finder')

    def comboal(w1,w2,w3,w4,ai):
        goto(w1,w3)
        goto(w2,w4)
        gov(w1,w2)
        gov(w3,w4)
        gov(w2,w3)
        shsa(w4,ai)

    def comboaq(w1,w2,w3,w4,w5,w6,ai):
        goto(w1,w3)
        goto(w2,w4)
        goto(w3,w5)
        goto(w4,w6)
        gov(w1,w2)       
        gov(w3,w4)
        gov(w5,w6)
        gov(w2,w3)
        gov(w4,w5)
        shsa(w6,ai)

    def comboac(w1,w2,w3,w4,w5,w6,w7,w8,ai):
        goto(w1,w3)
        goto(w2,w4)
        goto(w3,w5)
        goto(w4,w6)
        goto(w5,w7)
        goto(w6,w8)
        gov(w1,w2)       
        gov(w3,w4)
        gov(w5,w6)
        gov(w7,w8)
        gov(w2,w3)
        gov(w4,w5)
        gov(w6,w7)
        shsa(w8,ai)

    def shClose(event):
        win.destroy()
        '''
        win.bell()
        mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Arithmetic Pogression Rule Finder?')
        if mg == True:
            win.destroy()
        else:
            pass
            win.focus()
        '''

    def print_pttr_lc():
        try:
            t1 = float(n1.get())
            t2 = float(m1.get())
            p1 = float(n2.get())
            p2 = float(m2.get())
            a = p2 - p1
            b = t2 - t1
            d = a/b
            if t1 != 1:
                while t1 != 1:
                    t1 = t1 - 1
                    o = p1 - d
                    p1 = o
            else:
                o = p1
            u = o - d
            label5.configure(text="Position to Term rule: Un = " + str(d) + "(n) + (" + str(u) + ')')
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            n1.focus()
            


    def print_tttr_lc():
        try:
            t1 = float(n1.get())
            t2 = float(m1.get())
            p1 = float(n2.get())
            p2 = float(m2.get())
            a = p2 - p1
            b = t2 - t1
            d = a/b
            if t1 != 1:
                while t1 != 1:
                    t1 = t1 - 1
                    o = p1 - d
                    p1 = o
            else:
                o = p1
            label6.configure(text="Term to Term rule: U(n+1) = " + str(o) + ' + n(' + str(d) + ')')
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            n1.focus()

    def print_pttr_qc():
        try:
            t1 = float(x2.get())
            t2 = float(y2.get())
            t3 = float(z2.get())
            p1 = float(x1.get())
            p2 = float(y1.get())
            p3 = float(z1.get())
            d1_1 = t2 - t1
            d1_2 = t3 - t2
            d2 = d1_2 - d1_1
            pd1_1 = (p2**2) - (p1**2)
            pd1_2 = (p3**2) - (p2**2)
            pd2 = pd1_2 - pd1_1
            bd1 = p2 - p1
            bd2 = p3 - p2
            bd3 = bd2 - bd1
            td1 = bd3 * d1_1
            td2 = bd1 * d2
            atd1 = pd1_1 * bd3
            atd2 = pd2 * bd1
            atd3 = atd2 - atd1
            td3 = td2 - td1
            a = td3/atd3
            bpd = d1_1 - (a*pd1_1)
            b = bpd/bd1
            cad = (p1**2)*a
            cab = p1 * b
            c = t1 - (cad + cab)
            Qlabel_pttr.configure(text="Position to term rule: Un = (" + str(a) + ")n*n + (" + str(b) + ")n + (" + str(c) + ")")
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            x1.focus()

    def print_pttr_cc():
        try:
            t1 = float(ca2.get())
            t2 = float(cb2.get())
            t3 = float(cc2.get())
            t4 = float(cd2.get())
            p1 = float(ca1.get())
            p2 = float(cb1.get())
            p3 = float(cc1.get())
            p4 = float(cd1.get())
            d1_1 = t2-t1
            d1_2 = t3-t2
            d1_3 = t4-t3
            d2_1 = d1_2 - d1_1
            d2_2 = d1_3 - d1_2
            da = d2_2 - d2_1
            a = da/6
            d2V1_1 = (p2*p2*p2) - (p1*p1*p1)
            d2V1_2 = (p3*p3*p3) - (p2*p2*p2)
            d2V1 = d2V1_2 - d2V1_1
            db = d2_1 - (d2V1*a)
            b = db/2
            d1V1 = (p2*p2) - (p1*p1)
            c = d1_1 - ((d2V1_1*a) + (d1V1*b))
            d = t1 - (((p1*p1*p1)*a) + ((p1*p1)*b) + c)
            Clabel_pttr.configure(text="Position to Term rule: Un = (" + str(a) + ')n*n*n + (' + str(b) + ')n*n + (' + str(c) + ')n + (' + str(d) + ')')
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            n1.focus()

    def clear():
        v1.set(empty)
        v2.set(empty)
        v3.set(empty)
        v4.set(empty)
        label5.configure(text='')
        label6.configure(text='')
        label_help.configure(text='')
        n1.focus()

    def Qclear():
        Qv1.set(empty)
        Qv2.set(empty)
        Qv3.set(empty)
        Qv4.set(empty)
        Qv5.set(empty)
        Qv6.set(empty)
        Qlabel_pttr.configure(text='')
        Qlabel_help.configure(text='')
        x1.focus()
        
    def Cclear():
        Cv1.set(empty)
        Cv2.set(empty)
        Cv3.set(empty)
        Cv4.set(empty)
        Cv5.set(empty)
        Cv6.set(empty)
        Clabel_pttr.configure(text='')
        Clabel_help.configure(text='')
        ca1.focus()

    def lcHelpFunction():
        label_help.configure(text=' User\'s Guidelines:\n\tFirst type in the position of a known term and then type in the term itself.\n\tThen type in the position of a second known term and then type in the second term itself.\n\tAfter that select a button to view the position to term rule of the sequence.\n\tor the term to term rule of the sequence.\n\tYou can also quit the calculator and clear data entered.\nYou can also view the menubar for further commands.')
        mF1.focus()
        n1.focus()

    def qcHelpFunction():
        Qlabel_help.configure(text=' User\'s Guidelines:\n\tFirst type in the position of a known term and then type in the term itself.\n\tThen type in the position of a second known term and then type in the second term itself.\n\tRepeat for third position and third term.\n\tAfter that select a button to view the position to term rule of the sequence.\n\tYou can also quit the calculator and clear data entered.\nYou can also view the menubar for further commands.')
        mF2.focus()
        x1.focus()
    
    def ccHelpFunction():
        Clabel_help.configure(text='')
        Clabel_help.configure(text=' User\'s Guidelines:\n\tFirst type in the position of a known term and then type in the term itself.\n\tThen type in the position of a second known term and then type in the second term itself.\n\tRepeat for third, fourth position and third, fourth term.\n\tAfter that select a button to view the position to term rule of the sequence.\n\tYou can also quit the calculator and clear data entered.\nYou can also view the menubar for further commands.')

    def aboutFunction():
        label_help.configure(text='Arithmetic Calculator v2.6 - 2019\nDevolped and Published by Jaiwanth Karthi')
        Qlabel_help.configure(text='Arithmetic Calculator v2.6 - 2019\nDevolped and Published by Jaiwanth Karthi')
        Clabel_help.configure(text='Arithmetic Calculator v2.6 - 2019\nDevolped and Published by Jaiwanth Karthi')

    #HelpMenu code
    helpmenu = tk.Menu(menubar, tearoff=1)
    helpmenu.add_command(label='Linear Rule Finder Guidelines', command=lcHelpFunction)
    helpmenu.add_command(label='Quadratic Rule Finder Guidelines',command=qcHelpFunction)
    helpmenu.add_command(label='Cubic Sequence Rule Finder Guidelines', command=ccHelpFunction)
    helpmenu.add_separator()
    helpmenu.add_command(label='About', command=aboutFunction)
    menubar.add_cascade(label='Help', menu=helpmenu)

    #Linear calc code
    v1 = tk.DoubleVar()
    v2 = tk.DoubleVar()
    v3 = tk.DoubleVar()
    v4 = tk.DoubleVar()
    v1.set(empty)
    v2.set(empty)
    v3.set(empty)
    v4.set(empty)

    nb1 = ttk.Notebook(win)
    mF1 = ttk.Frame(nb1)
    nb1.add(mF1,text='Linear sequence calc')
    frame1 = ttk.LabelFrame(mF1)
    frame1.grid(column=0, row=0, sticky='E', columnspan=1, pady=2)
    frame2 = ttk.LabelFrame(mF1)
    frame2.grid(column=0, row=1, sticky='E', columnspan=1, pady=2)
    frame3 = ttk.LabelFrame(mF1)
    frame3.grid(column=1, row=0, sticky='E', columnspan=1, pady=2)
    frame4 = ttk.LabelFrame(mF1)
    frame4.grid(column=1, row=1, sticky='E', columnspan=1, pady=2)
    frameb = ttk.LabelFrame(mF1)
    frameb.grid(column=0, row=2, sticky='W', columnspan=4, pady=2)
    frame_ans = ttk.Frame(mF1)
    frame_ans.grid(column=0, row=3, sticky='W', columnspan=4, pady=4)
    frame_help = ttk.Frame(mF1)
    frame_help.grid(column=0, row=4, sticky='W', columnspan=4, pady=4)

    label1=ttk.Label(frame1, text = 'Enter 1st position: ')
    label1.grid(column=0,row=0)
    Hovertip(label1, '1st position is the known place of a term in the sequence.', hover_delay=1000)
    n1 = ttk.Entry(frame1, textvariable=v1)
    n1.grid(column=0, row=1, columnspan=2)
    Hovertip(n1, 'Enter the position in which the first term is placed at.', hover_delay=500)

    label2=ttk.Label(frame2, text = 'Enter 1st term: ')
    label2.grid(column=1,row=0)
    Hovertip(label2, '1st term is the number which has the 1st known position in a sequence.', hover_delay=1000)
    n2 = ttk.Entry(frame2, textvariable=v3)
    n2.grid(column=1, row=1)
    Hovertip(n2, 'Enter the first term resting at the first position.', hover_delay=500)

    label3=ttk.Label(frame3, text = 'Enter 2nd position: ')
    label3.grid(column=2,row=0)
    Hovertip(label3, '2nd position is the known place of another term in the sequence.', hover_delay=1000)
    m1 = ttk.Entry(frame3, textvariable=v2)
    m1.grid(column=2, row=1)
    Hovertip(m1, 'Enter the position in which the second term is placed at.', hover_delay=500)

    label4=ttk.Label(frame4, text = 'Enter 2nd term: ')
    label4.grid(column=3,row=0)
    Hovertip(label4, '2nd term is the number which has the 2nd known position in a sequence.', hover_delay=1000)
    m2 = ttk.Entry(frame4, textvariable=v4)
    m2.grid(column=3, row=1)
    Hovertip(m2, 'Enter the second term resting at the second position.', hover_delay=500)

    b1 = ttk.Button(frameb, text='Show Position to Term rule', command=print_pttr_lc)
    b1.grid(column=1,row=2)
    Hovertip(b1, 'Click here to display The position to term rule for the sequence entered.', hover_delay=500)
    b2 = ttk.Button(frameb, text='Show Term to Term rule', command=print_tttr_lc)
    b2.grid(column=2,row=2)
    Hovertip(b2, 'Click here to display The term to term rule for the sequence entered.', hover_delay=500)
    cb = ttk.Button(frameb, text='Clear', command=clear)
    cb.grid(column=0,row=2)
    Hovertip(cb, 'Click here to clear the answers and entries.', hover_delay=500)

    label5=ttk.Label(frame_ans)
    label5.grid(column=0,row=0)
    label6=ttk.Label(frame_ans)
    label6.grid(column=0,row=1)
    label_help=ttk.Label(frame_help)
    label_help.grid(column=0,row=0,sticky='W')

    comboal(n1,n2,m1,m2,print_pttr_lc)

    #Quadratic calc code
    Qv1 = tk.DoubleVar()
    Qv2 = tk.DoubleVar()
    Qv3 = tk.DoubleVar()
    Qv4 = tk.DoubleVar()
    Qv5 = tk.DoubleVar()
    Qv6 = tk.DoubleVar()
    Qv1.set(empty)
    Qv2.set(empty)
    Qv3.set(empty)
    Qv4.set(empty)
    Qv5.set(empty)
    Qv6.set(empty)

    mF2 = ttk.Frame(nb1)
    nb1.add(mF2,text='Quadratic sequence calc')
    Qframe1 = ttk.LabelFrame(mF2)
    Qframe1.grid(column=0, row=0, sticky='E', columnspan=1, pady=2)
    Qframe2 = ttk.LabelFrame(mF2)
    Qframe2.grid(column=0, row=1, sticky='E', columnspan=1, pady=2)
    Qframe3 = ttk.LabelFrame(mF2)
    Qframe3.grid(column=1, row=0, sticky='E', columnspan=1, pady=2)
    Qframe4 = ttk.LabelFrame(mF2)
    Qframe4.grid(column=1, row=1, sticky='E', columnspan=1, pady=2)
    Qframe5 = ttk.LabelFrame(mF2)
    Qframe5.grid(column=2, row=0, sticky='E', columnspan=1, pady=2)
    Qframe6 = ttk.LabelFrame(mF2)
    Qframe6.grid(column=2, row=1, sticky='E', columnspan=1, pady=2)
    Qframeb = ttk.LabelFrame(mF2)
    Qframeb.grid(column=0, row=2, sticky='W', columnspan=4, pady=2)
    Qframe_ans = ttk.Frame(mF2)
    Qframe_ans.grid(column=0, row=3, sticky='W', columnspan=4, pady=4)
    Qframe_help = ttk.Frame(mF2)
    Qframe_help.grid(column=0, row=4, sticky='W', columnspan=4, pady=4)

    Qlabel1=ttk.Label(Qframe1, text = 'Enter 1st position: ')
    Qlabel1.grid(column=0,row=0)
    Hovertip(Qlabel1, '1st position is the known place of a term in the sequence.', hover_delay=1000)
    x1 = ttk.Entry(Qframe1, textvariable=Qv1)
    x1.grid(column=0, row=1, columnspan=2)
    Hovertip(x1, 'Enter the position in which the first term is placed at.', hover_delay=500)

    Qlabel2=ttk.Label(Qframe2, text = 'Enter 1st term: ')
    Qlabel2.grid(column=0,row=0)
    Hovertip(Qlabel2, '1st term is the number which has the 1st known position in a sequence.', hover_delay=1000)
    x2 = ttk.Entry(Qframe2, textvariable=Qv2)
    x2.grid(column=0, row=1)
    Hovertip(x2, 'Enter the first term resting at the first position.', hover_delay=500)

    Qlabel3=ttk.Label(Qframe3, text = 'Enter 2nd position: ')
    Qlabel3.grid(column=0,row=0)
    Hovertip(Qlabel3, '2nd position is the known place of another term in the sequence.', hover_delay=1000)
    y1 = ttk.Entry(Qframe3, textvariable=Qv3)
    y1.grid(column=0, row=1)
    Hovertip(y1, 'Enter the position in which the second term is placed at.', hover_delay=500)

    Qlabel4=ttk.Label(Qframe4, text = 'Enter 2nd term: ')
    Qlabel4.grid(column=0,row=0)
    Hovertip(Qlabel4, '2nd term is the number which has the 2nd known position in a sequence.', hover_delay=1000)
    y2 = ttk.Entry(Qframe4, textvariable=Qv4)
    y2.grid(column=0, row=1)
    Hovertip(y2, 'Enter the second term resting at the second position.', hover_delay=500)

    Qlabel5=ttk.Label(Qframe5, text = 'Enter 3rd position: ')
    Qlabel5.grid(column=0,row=0)
    Hovertip(Qlabel5, ' term is the number which has the 2nd known position in a sequence.', hover_delay=1000)
    z1 = ttk.Entry(Qframe5, textvariable=Qv5)
    z1.grid(column=0, row=1)
    Hovertip(z1, '3rd position is the known place of another term in the sequence.', hover_delay=500)

    Qlabel6=ttk.Label(Qframe6, text = 'Enter 3rd term: ')
    Qlabel6.grid(column=0,row=0)
    Hovertip(Qlabel6, '3rd term is the number which has the 3rd known position in a sequence.', hover_delay=1000)
    z2 = ttk.Entry(Qframe6, textvariable=Qv6)
    z2.grid(column=0, row=1)
    Hovertip(z2, 'Enter the second term resting at the second position.', hover_delay=500)

    Qb1 = ttk.Button(Qframeb, text='Show Position to Term rule', command=print_pttr_qc)
    Qb1.grid(column=1,row=2)
    Hovertip(b1, 'Click here to display The position to term rule for the sequence entered.', hover_delay=500)
    Qcb = ttk.Button(Qframeb, text='Clear', command=Qclear)
    Qcb.grid(column=0,row=2)
    Hovertip(cb, 'Click here to clear the answers and entries.', hover_delay=500)

    Qlabel_pttr=ttk.Label(Qframe_ans)
    Qlabel_pttr.grid(column=0,row=0)
    Qlabel_help=ttk.Label(Qframe_help)
    Qlabel_help.grid(column=0,row=0,sticky='W')

    comboaq(x1,x2,y1,y2,z1,z2,print_pttr_qc)

    #Cubic calc code
    Cv1 = tk.DoubleVar()
    Cv2 = tk.DoubleVar()
    Cv3 = tk.DoubleVar()
    Cv4 = tk.DoubleVar()
    Cv5 = tk.DoubleVar()
    Cv6 = tk.DoubleVar()
    Cv7 = tk.DoubleVar()
    Cv8 = tk.DoubleVar()
    Cv1.set(empty)
    Cv2.set(empty)
    Cv3.set(empty)
    Cv4.set(empty)
    Cv5.set(empty)
    Cv6.set(empty)
    Cv7.set(empty)
    Cv8.set(empty)

    mF3 = ttk.Frame(nb1)
    nb1.add(mF3,text='Cubic sequence calc')
    Cframe1 = ttk.LabelFrame(mF3)
    Cframe1.grid(column=0, row=0, sticky='E', columnspan=1, pady=2)
    Cframe2 = ttk.LabelFrame(mF3)
    Cframe2.grid(column=0, row=1, sticky='E', columnspan=1, pady=2)
    Cframe3 = ttk.LabelFrame(mF3)
    Cframe3.grid(column=1, row=0, sticky='E', columnspan=1, pady=2)
    Cframe4 = ttk.LabelFrame(mF3)
    Cframe4.grid(column=1, row=1, sticky='E', columnspan=1, pady=2)
    Cframe5 = ttk.LabelFrame(mF3)
    Cframe5.grid(column=2, row=0, sticky='E', columnspan=1, pady=2)
    Cframe6 = ttk.LabelFrame(mF3)
    Cframe6.grid(column=2, row=1, sticky='E', columnspan=1, pady=2)
    Cframe7 = ttk.LabelFrame(mF3)
    Cframe7.grid(column=3, row=0, sticky='E', columnspan=1, pady=2)
    Cframe8 = ttk.LabelFrame(mF3)
    Cframe8.grid(column=3, row=1, sticky='E', columnspan=1, pady=2)
    Cframeb = ttk.LabelFrame(mF3)
    Cframeb.grid(column=0, row=2, sticky='W', columnspan=4, pady=2)
    Cframe_ans = ttk.Frame(mF3)
    Cframe_ans.grid(column=0, row=3, sticky='W', columnspan=4, pady=4)
    Cframe_help = ttk.Frame(mF3)
    Cframe_help.grid(column=0, row=4, sticky='W', columnspan=4, pady=4)

    Clabel1=ttk.Label(Cframe1, text = 'Enter 1st position: ')
    Clabel1.grid(column=0,row=0)
    Hovertip(Clabel1, '1st position is the known place of a term in the sequence.', hover_delay=1000)
    ca1 = ttk.Entry(Cframe1, textvariable=Cv1)
    ca1.grid(column=0, row=1, columnspan=2)
    Hovertip(ca1, 'Enter the position in which the first term is placed at.', hover_delay=500)

    Clabel2=ttk.Label(Cframe2, text = 'Enter 1st term: ')
    Clabel2.grid(column=1,row=0)
    Hovertip(Clabel2, '1st term is the number which has the 1st known position in a sequence.', hover_delay=1000)
    ca2 = ttk.Entry(Cframe2, textvariable=Cv2)
    ca2.grid(column=1, row=1)
    Hovertip(ca2, 'Enter the first term resting at the first position.', hover_delay=500)

    Clabel3=ttk.Label(Cframe3, text = 'Enter 2nd position: ')
    Clabel3.grid(column=2,row=0)
    Hovertip(Clabel3, '2nd position is the known place of another term in the sequence.', hover_delay=1000)
    cb1 = ttk.Entry(Cframe3, textvariable=Cv3)
    cb1.grid(column=2, row=1)
    Hovertip(cb1, 'Enter the position in which the second term is placed at.', hover_delay=500)

    Clabel4=ttk.Label(Cframe4, text = 'Enter 2nd term: ')
    Clabel4.grid(column=3,row=0)
    Hovertip(Clabel4, '2nd term is the number which has the 2nd known position in a sequence.', hover_delay=1000)
    cb2 = ttk.Entry(Cframe4, textvariable=Cv4)
    cb2.grid(column=3, row=1)
    Hovertip(cb2, 'Enter the second term resting at the second position.', hover_delay=500)

    Clabel5=ttk.Label(Cframe5, text = 'Enter 1st position: ')
    Clabel5.grid(column=0,row=0)
    Hovertip(Clabel5, '3rd position is the known place of the third known term in the sequence.', hover_delay=1000)
    cc1 = ttk.Entry(Cframe5, textvariable=Cv5)
    cc1.grid(column=0, row=1, columnspan=2)
    Hovertip(cc1, 'Enter the position in which the third term is placed at.', hover_delay=500)

    Clabel6=ttk.Label(Cframe6, text = 'Enter 1st term: ')
    Clabel6.grid(column=1,row=0)
    Hovertip(Clabel2, '3rd term is the number which has the 3rd known position in a sequence.', hover_delay=1000)
    cc2 = ttk.Entry(Cframe6, textvariable=Cv6)
    cc2.grid(column=1, row=1)
    Hovertip(cc2, 'Enter the third term resting at the third position.', hover_delay=500)

    Clabel7=ttk.Label(Cframe7, text = 'Enter 2nd position: ')
    Clabel7.grid(column=2,row=0)
    Hovertip(label3, '4th position is the known place of the fourth known term in the sequence.', hover_delay=1000)
    cd1 = ttk.Entry(Cframe7, textvariable=Cv7)
    cd1.grid(column=2, row=1)
    Hovertip(cd1, 'Enter the position in which the fourth term is placed at.', hover_delay=500)

    Clabel8=ttk.Label(Cframe8, text = 'Enter 2nd term: ')
    Clabel8.grid(column=3,row=0)
    Hovertip(label4, '4th term is the number which has the 4th known position in a sequence.', hover_delay=1000)
    cd2 = ttk.Entry(Cframe8, textvariable=Cv8)
    cd2.grid(column=3, row=1)
    Hovertip(cd2, 'Enter the fourth term resting at the fourth position.', hover_delay=500)

    Cb1 = ttk.Button(Cframeb, text='Show Position to Term rule', command=print_pttr_cc)
    Cb1.grid(column=1,row=2)
    Hovertip(Cb1, 'Click here to display The term to term rule for the sequence entered.', hover_delay=500)
    Ccb = ttk.Button(Cframeb, text='Clear', command=Cclear)
    Ccb.grid(column=0,row=2)
    Hovertip(Ccb, 'Click here to clear the answers and entries.', hover_delay=500)
    Clabel_pttr=ttk.Label(Cframe_ans)
    Clabel_pttr.grid(column=0,row=0)
    Clabel_help=ttk.Label(Cframe_help)
    Clabel_help.grid(column=0,row=0,sticky='W')

    nb1.grid(columnspan=1,column=0,row=0)

    comboac(ca1,ca2,cb1,cb2,cc1,cc2,cd1,cd2,print_pttr_cc)
    win.bind('<Control-q>',shClose)
    win.protocol('WM_DELETE_WINDOW',lambda:shClose(None))
    win.config(menu=menubar)
    n1.focus()
    win.mainloop()

def Calc_init():
    win = tk.Toplevel(root)
    win.title('The Calculator')

    def clear():
        var1.set(empty)
        var2.set(empty)
        output.configure(text='0')
        first_num.focus()

    def add():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            output.configure(text=num1+num2)
        except ValueError and _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()
            
    def subtract():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            output.configure(text=num1-num2)
        except ValueError and _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()

    def multiply():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            output.configure(text=num1*num2)
        except ValueError and _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()

    def divide():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            if num2 == 0:
                win.bell()
                messagebox.showerror(title='Division Error', message='You are dividing by Zero!\nEnter any other number to calculate.')
                win.focus()
            else:
                output.configure(text=num1/num2)
        except ValueError and _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()

    def power():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            output.configure(text=num1**num2)
        except ValueError and _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()

    def nthroot():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            if num2 == 0:
                win.bell()
                messagebox.showerror(title='Root Error', message='Zero cannot be a root of a number!\nEnter any other number to calculate.')
                win.focus()
            else:
                output.configure(text=num1**(1/num2))
        except ValueError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()

    def percent():
        try:
            num1 = float(var1.get())
            num2 = float(var2.get())
            output.configure(text=num2/100*num1)
        except ValueError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input.')
            win.focus()        

    def close():
        win.destroy()
        '''
        msg = messagebox.askyesno(title='Quit', message='Are you sure you want to quit the Calculator?')
        if msg == True:
            win.destroy()
        else:
            pass
            win.focus()
            first_num.focus()
        '''

    var1 = tk.DoubleVar()
    var2 = tk.DoubleVar()
    var1.set(empty)
    var2.set(empty)

    frame_1 = ttk.Frame(win)
    frame_1.grid(column=0, row=0, sticky='E')

    label_1 = ttk.Label(frame_1, text='Enter the first number (a)')
    label_1.grid(column=0, row=0, sticky='W')

    first_num = ttk.Entry(frame_1, textvariable=var1)
    first_num.grid(column=0, row=1)
    Hovertip(first_num, 'Enter the first number to perform the calculation', hover_delay=750)

    frame_2 = ttk.Frame(win)
    frame_2.grid(column=1, row=0, sticky='E')

    label_2 = ttk.Label(frame_2, text='Enter the second number (b)')
    label_2.grid(column=0, row=0, sticky='W')

    second_num = ttk.Entry(frame_2, textvariable=var2)
    second_num.grid(column=0, row=1)
    Hovertip(second_num, 'Enter the second number to perform the calculation', hover_delay=750)

    frame_3 = ttk.Frame(win)
    frame_3.grid(column=0, row=1, columnspan=3, pady=3)

    Add = ttk.Button(frame_3, text='Add', command=add)
    Add.grid(column=0, row=0)
    Hovertip(Add, 'Add the value \'a\' and \'b\'', hover_delay=750)

    Subtract = ttk.Button(frame_3, text='Subtract', command=subtract)
    Subtract.grid(column=1, row=0)
    Hovertip(Subtract, 'Subtract the value \'b\' from \'a\'', hover_delay=750)

    Multiply = ttk.Button(frame_3, text='Multiply', command=multiply)
    Multiply.grid(column=2, row=0)
    Hovertip(Multiply, 'Multiply the values \'a\' and \'b\'', hover_delay=750)

    Divide = ttk.Button(frame_3, text='Divide', command=divide)
    Divide.grid(column=0, row=1)
    Hovertip(Divide, 'Divide the value \'a\' by \'b\'', hover_delay=750)

    Power = ttk.Button(frame_3, text='Power', command=power)
    Power.grid(column=1, row=1)
    Hovertip(Power, 'Value \'a\' to the power \'b\'', hover_delay=750)

    NthRoot = ttk.Button(frame_3, text='Nth Root', command=nthroot)
    NthRoot.grid(column=2, row=1)
    Hovertip(NthRoot, 'Result to the power \'b\' equals \'a\'', hover_delay=750)

    Percent = ttk.Button(frame_3, text='Percent', command=percent)
    Percent.grid(column=0, row=2, columnspan=4)
    Hovertip(Percent, 'Result equals the \'b\' percent of \'a\'', hover_delay=750)

    frame_4 = ttk.Frame(win)
    frame_4.grid(column=0, row=5, columnspan=3)

    result = ttk.Label(frame_4, text='Result:')
    result.grid(column=0, row=0)

    output = ttk.Label(frame_4, text='0')
    output.grid(column=1, row=0, columnspan=2)

    frame_5 = ttk.Frame(win)
    frame_5.grid(column=0, row=6, columnspan=3)

    clear = ttk.Button(frame_5, text='Clear', command=clear)
    clear.grid(column=0, row=1, sticky='E')
    Hovertip(clear, 'Clear all the inputs and the result', hover_delay=750)

    quitbutton = ttk.Button(frame_5, text='Quit', command=close)
    quitbutton.grid(column=1, row=1, sticky='E')
    Hovertip(quitbutton, 'Quit this application', hover_delay=750)

    win.mainloop()

def Geo_Calc_init():
    win = tk.Toplevel(root)
    menubar = tk.Menu(win)
    win.title('Geometric Progression Rule Finder')

    def shClose(event):
        win.destroy()
        '''
        win.bell()
        mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Geometric Pogression Rule Finder?')
        if mg == True:
            win.destroy()
        else:
            pass
            win.focus()
        '''

    def comboql(w1,w2,w3,w4,ai):
        goto(w1,w3)
        goto(w2,w4)
        gov(w1,w2)
        gov(w3,w4)
        gov(w2,w3)
        shsa(w4,ai)

    def print_pttr_lc():
        try:
            p1 = float(n1.get())
            p2 = float(m1.get())
            t1 = float(n2.get())
            t2 = float(m2.get())
            dt = t2/t1
            dp1 = p2-p1
            dp = 1/dp1
            d = dt**dp
            if p1 != 1:
                while p1 != 1:
                    t1 = t1/d
                    p1 = p1 - 1
                    o = t1
            else:
                o = t1
            label5.configure(text="Position to Term rule: Un = " + str(d) + "^(n-1) x (" + str(o) + ')')
            n1.focus()
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            n1.focus()

    def print_tttr_lc():
        try:
            p1 = float(n1.get())
            p2 = float(m1.get())
            t1 = float(n2.get())
            t2 = float(m2.get())
            dt = t2/t1
            dp1 = p2-p1
            dp = 1/dp1
            d = dt**dp
            label5.configure(text="Term to Term rule: Un+1 = Un*" + str(d))
            n1.focus()
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            n1.focus()

    def clear():
        v1.set(empty)
        v2.set(empty)
        v3.set(empty)
        v4.set(empty)
        label5.configure(text='')
        label6.configure(text='')
        label_help.configure(text='')
        n1.focus()

    def lcHelpFunction():
        label_help.configure(text='')
        label_help.configure(text=' User\'s Guidelines:\n\tFirst type in the position of a known term and then type in the term itself.\n\tThen type in the position of a second known term and then type in the second term itself.\n\tAfter that select a button to view the position to term rule of the sequence.\n\tYou can also quit the calculator and clear data entered.\nYou can view the menubar for further commands.')
        n1.focus()

    def aboutFunction():
        label_help.configure(text='')
        label_help.configure(text='Arithmetic Calculator v2.6 - 2019\nDevolped and Published by Jaiwanth Karthi\nCredits : Pradnesh, Mr.Jeeva')
        n1.focus()

    #HelpMenu code
    helpmenu = tk.Menu(menubar, tearoff=1)
    helpmenu.add_command(label='Linear Rule Finder Guidelines', command=lcHelpFunction)
    helpmenu.add_separator()
    helpmenu.add_command(label='About', command=aboutFunction)
    menubar.add_cascade(label='Help', menu=helpmenu)

    #Linear calc code
    v1 = tk.DoubleVar()
    v2 = tk.DoubleVar()
    v3 = tk.DoubleVar()
    v4 = tk.DoubleVar()
    v1.set(empty)
    v2.set(empty)
    v3.set(empty)
    v4.set(empty)

    nb1 = ttk.Notebook(win)
    mF1 = ttk.Frame(nb1)
    nb1.add(mF1,text='Linear sequence calc')
    frame1 = ttk.LabelFrame(mF1)
    frame1.grid(column=0, row=0, sticky='E', columnspan=1, pady=2)
    frame2 = ttk.LabelFrame(mF1)
    frame2.grid(column=0, row=1, sticky='E', columnspan=1, pady=2)
    frame3 = ttk.LabelFrame(mF1)
    frame3.grid(column=1, row=0, sticky='E', columnspan=1, pady=2)
    frame4 = ttk.LabelFrame(mF1)
    frame4.grid(column=1, row=1, sticky='E', columnspan=1, pady=2)
    frameb = ttk.LabelFrame(mF1)
    frameb.grid(column=0, row=2, sticky='W', columnspan=4, pady=2)
    frame_ans = ttk.Frame(mF1)
    frame_ans.grid(column=0, row=3, sticky='W', columnspan=4, pady=4)
    frame_help = ttk.Frame(mF1)
    frame_help.grid(column=0, row=4, sticky='W', columnspan=4, pady=4)

    label1=ttk.Label(frame1, text = 'Enter 1st position: ')
    label1.grid(column=0,row=0)
    Hovertip(label1, '1st position is the known place of a term in the sequence.', hover_delay=1000)
    n1 = ttk.Entry(frame1, textvariable=v1)
    n1.grid(column=0, row=1, columnspan=2)
    Hovertip(n1, 'Enter the position in which the first term is placed at.', hover_delay=500)

    label2=ttk.Label(frame2, text = 'Enter 1st term: ')
    label2.grid(column=1,row=0)
    Hovertip(label2, '1st term is the number which has the 1st known position in a sequence.', hover_delay=1000)
    n2 = ttk.Entry(frame2, textvariable=v3)
    n2.grid(column=1, row=1)
    Hovertip(n2, 'Enter the first term resting at the first position.', hover_delay=500)

    label3=ttk.Label(frame3, text = 'Enter 2nd position: ')
    label3.grid(column=2,row=0)
    Hovertip(label3, '2nd position is the known place of another term in the sequence.', hover_delay=1000)
    m1 = ttk.Entry(frame3, textvariable=v2)
    m1.grid(column=2, row=1)
    Hovertip(m1, 'Enter the position in which the second term is placed at.', hover_delay=500)

    label4=ttk.Label(frame4, text = 'Enter 2nd term: ')
    label4.grid(column=3,row=0)
    Hovertip(label4, '2nd term is the number which has the 2nd known position in a sequence.', hover_delay=1000)
    m2 = ttk.Entry(frame4, textvariable=v4)
    m2.grid(column=3, row=1)
    Hovertip(m2, 'Enter the second term resting at the second position.', hover_delay=500)

    b1 = ttk.Button(frameb, text='Show Position to Term rule', command=print_pttr_lc)
    b1.grid(column=1,row=0)
    Hovertip(b1, 'Click here to display The position to term rule for the sequence entered.', hover_delay=500)
    cb = ttk.Button(frameb, text='Clear', command=clear)
    cb.grid(column=0,row=0)
    Hovertip(cb, 'Click here to clear the answers and entries.', hover_delay=500)

    label5=ttk.Label(frame_ans)
    label5.grid(column=0,row=0)
    label6=ttk.Label(frame_ans)
    label6.grid(column=0,row=1)
    label_help=ttk.Label(frame_help)
    label_help.grid(column=0,row=0,sticky='W')

    comboql(n1,n2,m1,m2,print_pttr_lc)

    nb1.grid(columnspan=1,column=0,row=0)

    win.bind('<Control-q>',shClose)
    win.protocol('WM_DELETE_WINDOW',lambda:shClose(None))
    win.config(menu=menubar)
    n1.focus()
    win.mainloop()

def iCalc_init():
    def helpFunc():
        pass

    def aboutFunc():
        pass

    win = tk.Toplevel(root)
    menubar = tk.Menu(win)
    win.title('Interest calculator')

    nb = ttk.Notebook(win)
    mF1 = ttk.Frame(nb)
    nb.add(mF1,text='Simple Interest calc')
    mF2 = ttk.Frame(nb)
    nb.add(mF2,text='Compound Interest calc')

    helpmenu = tk.Menu(menubar, tearoff=1)
    helpmenu.add_command(label='General Help', command=helpFunc)
    helpmenu.add_command(label='About', command=aboutFunc)
    menubar.add_cascade(label='Help', menu=helpmenu)

    empty = ' '

    #functions and classes
    def close_win():
        win.destroy()
        '''
        win.bell()
        mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Interest Calulator?')
        if mg == True:
            win.destroy()
        else:
            pass
            s1_1.focus()
        '''

    def ssClear():
        ss1.set(empty)
        ss2.set(empty)
        ss3.set(empty)
        ss4.set(empty)
        ssAL.configure(text='Simple Interest: ')
        s1_1.focus()

    def ssAns():
        try:
            try:
                n1 = float(s1_1.get())
                n2 = float(s1_2.get())
                n3 = float(s1_3.get())
                a = (n1*n2*n3)/100
                ssAL.configure(text='Simple Interest: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(s1_1.get())
                n2 = float(s1_4.get())
                a = n2 - n1
                ssAL.configure(text='Simple Interest: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            s2_1.focus()

    def spClear():
        sp1.set(empty)
        sp2.set(empty)
        sp3.set(empty)
        sp4.set(empty)
        spAL.configure(text='Principle: ')
        s2_1.focus()

    def spAns():
        try:
            try:
                n1 = float(s2_1.get())
                n2 = float(s2_2.get())
                n3 = float(s2_3.get())
                a = (100*n1)/(n2*n3)
                spAL.configure(text='Principle: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(s2_1.get())
                n2 = float(s2_4.get())
                a = n2 - n1
                spAL.configure(text='Principle: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            s2_1.focus()

    def siClear():
        si1.set(empty)
        si2.set(empty)
        si3.set(empty)
        siAL.configure(text='Interest: ')
        s3_1.focus()

    def siAns():
        try:
            n1 = float(s3_1.get())
            n2 = float(s3_2.get())
            n3 = float(s3_3.get())
            a = (100*n2)/(n1*n3)
            siAL.configure(text='Interest: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            s3_1.focus()

    def stClear():
        st1.set(empty)
        st2.set(empty)
        st3.set(empty)
        stAL.configure(text='Time: ')
        s4_1.focus()

    def stAns():
        try:
            n1 = float(s4_1.get())
            n2 = float(s4_2.get())
            n3 = float(s4_3.get())
            a = (100*n3)/(n2*n1)
            stAL.configure(text='Time: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            s4_1.focus()

    def saClear():
        sa1.set(empty)
        sa2.set(empty)
        sa3.set(empty)
        sa4.set(empty)
        saAL.configure(text='Amount: ')
        s5_1.focus()

    def saAns():
        try:
            try:
                n1 = float(s5_1.get())
                n2 = float(s5_4.get())
                a = n2 + n1
                saAL.configure(text='Amount: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(s5_1.get())
                n2 = float(s5_2.get())
                n3 = float(s5_3.get())
                a = ((n1*n2*n3)/100) + n1
                saAL.configure(text='Amount: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            s5_1.focus()

    #
    def csClear():
        cs1.set(empty)
        cs2.set(empty)
        cs3.set(empty)
        cs4.set(empty)
        csAL.configure(text='Compound Interest: ')
        c1_1.focus()

    def csAns():
        try:
            try:
                n1 = float(c1_1.get())
                n2 = float(c1_4.get())
                a = n2 - n1
                csAL.configure(text='Compound Interest: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(c1_1.get())
                n2 = float(c1_2.get())
                n3 = float(c1_3.get())
                a = (n1*((1 + (n2/100))**n3)) - n1
                csAL.configure(text='Compound Interest: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            c1_1.focus()

    def cpClear():
        cp1.set(empty)
        cp2.set(empty)
        cp3.set(empty)
        cp4.set(empty)
        cpAL.configure(text='Principle: ')
        c2_1.focus()

    def cpAns():
        try:
            try:
                n1 = float(c2_1.get())
                n2 = float(c2_4.get())
                a = n2 - n1
                cpAL.configure(text='Principle: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(c2_2.get())
                n2 = float(c2_3.get())
                n3 = float(c2_4.get())
                a = n3/((1 + (n1/100))**n2)
                cpAL.configure(text='Principle: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            c2_1.focus()

    def ciClear():
        ci1.set(empty)
        ci2.set(empty)
        ci3.set(empty)
        ci4.set(empty)
        ciAL.configure(text='Interest: ')
        c3_1.focus()

    def ciAns():
        try:
            try:
                n1 = float(c3_1.get())
                n2 = float(c3_3.get())
                n3 = float(c3_4.get())
                a = 100 * (((n3/n1)**(1/n2)) - 1)
                ciAL.configure(text='Interest: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(c3_1.get())
                n2 = float(c3_2.get())
                n3 = float(c3_3.get())
                a = 100 * ((((n2+n1)/n1)**(1/n3)) - 1)
                ciAL.configure(text='Interest: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            c2_1.focus()

    def ctClear():
        ct1.set(empty)
        ct2.set(empty)
        ct3.set(empty)
        ct4.set(empty)
        ctAL.configure(text='Time: ')
        c4_1.focus()

    def ctAns():
        try:
            try:
                n1 = float(c4_1.get())
                n2 = float(c4_2.get())
                n3 = float(c4_4.get())
                v = 1 + (n2/100)
                v1 = n3/n1
                a = math.log(v1, v)
                ctAL.configure(text='Time: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(c4_1.get())
                n2 = float(c4_2.get())
                n3 = float(c4_3.get())
                v = 1 + (n2/100)
                v1 = n3 + n1
                v2 = v1/n1
                a = math.log(v2, v)
                ctAL.configure(text='Time: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            c4_1.focus()

    def caClear():
        ca1.set(empty)
        ca2.set(empty)
        ca3.set(empty)
        ca4.set(empty)
        caAL.configure(text='Amount: ')
        c5_1.focus()

    def caAns():
        try:
            try:
                n1 = float(c5_1.get())
                n2 = float(c5_2.get())
                n3 = float(c5_3.get())
                a = n1 * ((1 + (n2/100))**n3)
                caAL.configure(text='Amount: ' + str(a))
            except ValueError or _tkinter.TclError:
                n1 = float(c5_1.get())
                n2 = float(c5_4.get())
                a = n2 + n1
                caAL.configure(text='Amount: ' + str(a))
        except ValueError or _tkinter.TclError:
            win.bell()
            messagebox.showerror(title='Input Error', message='Input isn\'t correct to calculate!\nType in a correct input,\ncontaining only numbers.')
            c5_1.focus()

    def combo(w1,w2,w3,ai):
        goto(w1,w2)
        goto(w2,w3)
        shsa(w3,ai)

    def cmbe(w1,w2,w3,w4,ai):
        goto(w1,w2)
        goto(w2,w3)
        goto(w3,w4)
        shsa(w4,ai)

    def shClose(event):
        win.destroy()
        '''
        win.bell()
        mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Interest Calulator?')
        if mg == True:
            win.destroy()
        else:
            pass
            win.focus()
            s1_1.focus()
        '''

    #Simple section
    ss1 = tk.DoubleVar()
    ss2 = tk.DoubleVar()
    ss3 = tk.DoubleVar()
    ss4 = tk.DoubleVar()
    ss1.set(empty)
    ss2.set(empty)
    ss3.set(empty)
    ss4.set(empty)
    sp1 = tk.DoubleVar()
    sp2 = tk.DoubleVar()
    sp3 = tk.DoubleVar()
    sp4 = tk.DoubleVar()
    sp1.set(empty)
    sp2.set(empty)
    sp3.set(empty)
    sp4.set(empty)
    si1 = tk.DoubleVar()
    si2 = tk.DoubleVar()
    si3 = tk.DoubleVar()
    si1.set(empty)
    si2.set(empty)
    si3.set(empty)
    st1 = tk.DoubleVar()
    st2 = tk.DoubleVar()
    st3 = tk.DoubleVar()
    st1.set(empty)
    st2.set(empty)
    st3.set(empty)
    sa1 = tk.DoubleVar()
    sa2 = tk.DoubleVar()
    sa3 = tk.DoubleVar()
    sa4 = tk.DoubleVar()
    sa1.set(empty)
    sa2.set(empty)
    sa3.set(empty)
    sa4.set(empty)

    snb = ttk.Notebook(mF1)
    sF1 = ttk.Frame(snb)
    snb.add(sF1,text = 'Simple Interest Finder')
    sF2 = ttk.Frame(snb)
    snb.add(sF2,text = 'Principle Finder')
    sF3 = ttk.Frame(snb)
    snb.add(sF3,text = 'Interest (Rate) Finder')
    sF4 = ttk.Frame(snb)
    snb.add(sF4,text = 'Time Finder')
    sF5 = ttk.Frame(snb)
    snb.add(sF5,text = 'Total Amount Finder')

    ssLF = ttk.Frame(sF1)
    ssLF.grid(column=0,row=0)
    ssAF = ttk.Frame(sF1)
    ssAF.grid(column=0,row=2)
    ssBF = ttk.Frame(sF1)
    ssBF.grid(column=0,row=1)

    spLF = ttk.Frame(sF2)
    spLF.grid(column=0,row=0)
    spAF = ttk.Frame(sF2)
    spAF.grid(column=0,row=2)
    spBF = ttk.Frame(sF2)
    spBF.grid(column=0,row=1)

    siLF = ttk.Frame(sF3)
    siLF.grid(column=0,row=0)
    siAF = ttk.Frame(sF3)
    siAF.grid(column=0,row=2)
    siBF = ttk.Frame(sF3)
    siBF.grid(column=0,row=1)

    stLF = ttk.Frame(sF4)
    stLF.grid(column=0,row=0)
    stAF = ttk.Frame(sF4)
    stAF.grid(column=0,row=2)
    stBF = ttk.Frame(sF4)
    stBF.grid(column=0,row=1)

    saLF = ttk.Frame(sF5)
    saLF.grid(column=0,row=0)
    saAF = ttk.Frame(sF5)
    saAF.grid(column=0,row=2)
    saBF = ttk.Frame(sF5)
    saBF.grid(column=0,row=1)

    #
    sslabel1=ttk.Label(ssLF, text = 'Enter Principle: ')
    sslabel1.grid(column=0,row=0)
    Hovertip(sslabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    s1_1 = ttk.Entry(ssLF, textvariable=ss1)
    s1_1.grid(column=0, row=1)
    Hovertip(s1_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    sslabel2=ttk.Label(ssLF, text = 'Enter Interest(Rate): ')
    sslabel2.grid(column=1,row=0)
    Hovertip(sslabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    s1_2 = ttk.Entry(ssLF, textvariable=ss2)
    s1_2.grid(column=1, row=1)
    Hovertip(s1_2, 'Enter the Interest or Rate.', hover_delay=1000)

    sslabel3=ttk.Label(ssLF, text = 'Enter Time: ')
    sslabel3.grid(column=2,row=0)
    Hovertip(sslabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    s1_3 = ttk.Entry(ssLF, textvariable=ss3)
    s1_3.grid(column=2, row=1)
    Hovertip(s1_3, 'Enter the time or duration.', hover_delay=1000)

    sslabel4=ttk.Label(ssLF, text = 'Enter Amount: ')
    sslabel4.grid(column=3,row=0)
    Hovertip(sslabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    s1_4 = ttk.Entry(ssLF, textvariable=ss4)
    s1_4.grid(column=3, row=1)
    Hovertip(s1_4, 'Enter the amount.', hover_delay=1000)

    ssAL = ttk.Label(ssAF,text='Simple Interest: ')
    ssAL.grid(column=0,row=0)

    sscb = ttk.Button(ssBF,text='Clear',command=ssClear)
    sscb.grid(column=0,row=0)
    ssmb = ttk.Button(ssBF,text='Show Answer',command=ssAns)
    ssmb.grid(column=1,row=0)
    ssqb = ttk.Button(ssBF,text='Quit',command=close_win)
    ssqb.grid(column=2,row=0)

    #
    splabel1=ttk.Label(spLF, text = 'Enter Simple Interest: ')
    splabel1.grid(column=0,row=0)
    Hovertip(splabel1, 'Simple Interest is the total interest.', hover_delay=1000)
    s2_1 = ttk.Entry(spLF, textvariable=sp1)
    s2_1.grid(column=0, row=1)
    Hovertip(s2_1, 'Enter the Simple Interest.', hover_delay=1000)

    splabel2=ttk.Label(spLF, text = 'Enter Interest(Rate): ')
    splabel2.grid(column=1,row=0)
    Hovertip(splabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    s2_2 = ttk.Entry(spLF, textvariable=sp2)
    s2_2.grid(column=1, row=1)
    Hovertip(s2_2, 'Enter the Interest or Rate.', hover_delay=1000)

    splabel3=ttk.Label(spLF, text = 'Enter Time: ')
    splabel3.grid(column=2,row=0)
    Hovertip(splabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    s2_3 = ttk.Entry(spLF, textvariable=sp3)
    s2_3.grid(column=2, row=1)
    Hovertip(s2_3, 'Enter the time or duration.', hover_delay=1000)

    splabel4=ttk.Label(spLF, text = 'Enter Amount: ')
    splabel4.grid(column=3,row=0)
    Hovertip(splabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    s2_4 = ttk.Entry(spLF, textvariable=sp4)
    s2_4.grid(column=3, row=1)
    Hovertip(s2_4, 'Enter the amount.', hover_delay=1000)

    spAL = ttk.Label(spAF,text='Principle: ')
    spAL.grid(column=0,row=0)

    spcb = ttk.Button(spBF,text='Clear',command=spClear)
    spcb.grid(column=0,row=0)
    spmb = ttk.Button(spBF,text='Show Answer',command=spAns)
    spmb.grid(column=1,row=0)
    spqb = ttk.Button(spBF,text='Quit',command=close_win)
    spqb.grid(column=2,row=0)

    #
    silabel1=ttk.Label(siLF, text = 'Enter Principle: ')
    silabel1.grid(column=0,row=0)
    Hovertip(silabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    s3_1 = ttk.Entry(siLF, textvariable=si1)
    s3_1.grid(column=0, row=1)
    Hovertip(s3_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    silabel2=ttk.Label(siLF, text = 'Enter Simple Interest: ')
    silabel2.grid(column=1,row=0)
    Hovertip(silabel2, 'Simple Interest is the total interest.', hover_delay=1000)
    s3_2 = ttk.Entry(siLF, textvariable=si2)
    s3_2.grid(column=1, row=1)
    Hovertip(s3_2, 'Enter the Simple Interest.', hover_delay=1000)

    silabel3=ttk.Label(siLF, text = 'Enter Time: ')
    silabel3.grid(column=2,row=0)
    Hovertip(silabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    s3_3 = ttk.Entry(siLF, textvariable=si3)
    s3_3.grid(column=2, row=1)
    Hovertip(s3_3, 'Enter the time or duration.', hover_delay=1000)

    siAL = ttk.Label(siAF,text='Interest: ')
    siAL.grid(column=0,row=0)

    sicb = ttk.Button(siBF,text='Clear',command=siClear)
    sicb.grid(column=0,row=0)
    simb = ttk.Button(siBF,text='Show Answer',command=siAns)
    simb.grid(column=1,row=0)
    siqb = ttk.Button(siBF,text='Quit',command=close_win)
    siqb.grid(column=2,row=0)

    #
    stlabel1=ttk.Label(stLF, text = 'Enter Principle: ')
    stlabel1.grid(column=0,row=0)
    Hovertip(stlabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    s4_1 = ttk.Entry(stLF, textvariable=st1)
    s4_1.grid(column=0, row=1)
    Hovertip(s4_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    stlabel2=ttk.Label(stLF, text = 'Enter Interest(Rate): ')
    stlabel2.grid(column=1,row=0)
    Hovertip(stlabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    s4_2 = ttk.Entry(stLF, textvariable=st2)
    s4_2.grid(column=1, row=1)
    Hovertip(s4_2, 'Enter the Interest or Rate.', hover_delay=1000)

    stlabel3=ttk.Label(stLF, text = 'Enter Simple Interest: ')
    stlabel3.grid(column=2,row=0)
    Hovertip(stlabel3, 'Simple Interest is the total interest.', hover_delay=1000)
    s4_3 = ttk.Entry(stLF, textvariable=st3)
    s4_3.grid(column=2, row=1)
    Hovertip(s4_3, 'Enter the Simple Interest.', hover_delay=1000)

    stAL = ttk.Label(stAF,text='Time: ')
    stAL.grid(column=0,row=0)

    stcb = ttk.Button(stBF,text='Clear',command=stClear)
    stcb.grid(column=0,row=0)
    stmb = ttk.Button(stBF,text='Show Answer',command=stAns)
    stmb.grid(column=1,row=0)
    stqb = ttk.Button(stBF,text='Quit',command=close_win)
    stqb.grid(column=2,row=0)

    #
    salabel1=ttk.Label(saLF, text = 'Enter Principle: ')
    salabel1.grid(column=0,row=0)
    Hovertip(salabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    s5_1 = ttk.Entry(saLF, textvariable=sa1)
    s5_1.grid(column=0, row=1)
    Hovertip(s5_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    salabel2=ttk.Label(saLF, text = 'Enter Interest(Rate): ')
    salabel2.grid(column=1,row=0)
    Hovertip(salabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    s5_2 = ttk.Entry(saLF, textvariable=sa2)
    s5_2.grid(column=1, row=1)
    Hovertip(s5_2, 'Enter the Interest or Rate.', hover_delay=1000)

    salabel3=ttk.Label(saLF, text = 'Enter Time: ')
    salabel3.grid(column=2,row=0)
    Hovertip(salabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    s5_3 = ttk.Entry(saLF, textvariable=sa3)
    s5_3.grid(column=2, row=1)
    Hovertip(s5_3, 'Enter the time or duration.', hover_delay=1000)

    salabel4=ttk.Label(saLF, text = 'Enter Simple Interest: ')
    salabel4.grid(column=3,row=0)
    Hovertip(salabel4, 'Simple Interest is the total interest.', hover_delay=1000)
    s5_4 = ttk.Entry(saLF, textvariable=sa4)
    s5_4.grid(column=3, row=1)
    Hovertip(s5_4, 'Enter the Simple Interest.', hover_delay=1000)

    saAL = ttk.Label(saAF,text='Amount: ')
    saAL.grid(column=0,row=0)

    sacb = ttk.Button(saBF,text='Clear',command=saClear)
    sacb.grid(column=0,row=0)
    samb = ttk.Button(saBF,text='Show Answer',command=saAns)
    samb.grid(column=1,row=0)
    saqb = ttk.Button(saBF,text='Quit',command=close_win)
    saqb.grid(column=2,row=0)

    snb.grid(column=0,row=0)

    #Compound Section
    cs1 = tk.DoubleVar()
    cs2 = tk.DoubleVar()
    cs3 = tk.DoubleVar()
    cs4 = tk.DoubleVar()
    cs1.set(empty)
    cs2.set(empty)
    cs3.set(empty)
    cs4.set(empty)
    cp1 = tk.DoubleVar()
    cp2 = tk.DoubleVar()
    cp3 = tk.DoubleVar()
    cp4 = tk.DoubleVar()
    cp1.set(empty)
    cp2.set(empty)
    cp3.set(empty)
    cp4.set(empty)
    ci1 = tk.DoubleVar()
    ci2 = tk.DoubleVar()
    ci3 = tk.DoubleVar()
    ci4 = tk.DoubleVar()
    ci1.set(empty)
    ci2.set(empty)
    ci3.set(empty)
    ci4.set(empty)
    ct1 = tk.DoubleVar()
    ct2 = tk.DoubleVar()
    ct3 = tk.DoubleVar()
    ct4 = tk.DoubleVar()
    ct1.set(empty)
    ct2.set(empty)
    ct3.set(empty)
    ct4.set(empty)
    ca1 = tk.DoubleVar()
    ca2 = tk.DoubleVar()
    ca3 = tk.DoubleVar()
    ca4 = tk.DoubleVar()
    ca1.set(empty)
    ca2.set(empty)
    ca3.set(empty)
    ca4.set(empty)

    cnb = ttk.Notebook(mF2)
    cF1 = ttk.Frame(cnb)
    cnb.add(cF1,text = 'Compound Interest Finder')
    cF2 = ttk.Frame(cnb)
    cnb.add(cF2,text = 'Principle Finder')
    cF3 = ttk.Frame(cnb)
    cnb.add(cF3,text = 'Interest (Rate) Finder')
    cF4 = ttk.Frame(cnb)
    cnb.add(cF4,text = 'Time Finder')
    cF5 = ttk.Frame(cnb)
    cnb.add(cF5,text = 'Total Amount Finder')

    csLF = ttk.Frame(cF1)
    csLF.grid(column=0,row=0)
    csAF = ttk.Frame(cF1)
    csAF.grid(column=0,row=2)
    csBF = ttk.Frame(cF1)
    csBF.grid(column=0,row=1)

    cpLF = ttk.Frame(cF2)
    cpLF.grid(column=0,row=0)
    cpAF = ttk.Frame(cF2)
    cpAF.grid(column=0,row=2)
    cpBF = ttk.Frame(cF2)
    cpBF.grid(column=0,row=1)

    ciLF = ttk.Frame(cF3)
    ciLF.grid(column=0,row=0)
    ciAF = ttk.Frame(cF3)
    ciAF.grid(column=0,row=2)
    ciBF = ttk.Frame(cF3)
    ciBF.grid(column=0,row=1)

    ctLF = ttk.Frame(cF4)
    ctLF.grid(column=0,row=0)
    ctAF = ttk.Frame(cF4)
    ctAF.grid(column=0,row=2)
    ctBF = ttk.Frame(cF4)
    ctBF.grid(column=0,row=1)

    caLF = ttk.Frame(cF5)
    caLF.grid(column=0,row=0)
    caAF = ttk.Frame(cF5)
    caAF.grid(column=0,row=2)
    caBF = ttk.Frame(cF5)
    caBF.grid(column=0,row=1)

    #
    cslabel1=ttk.Label(csLF, text = 'Enter Principle: ')
    cslabel1.grid(column=0,row=0)
    Hovertip(cslabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    c1_1 = ttk.Entry(csLF, textvariable=cs1)
    c1_1.grid(column=0, row=1)
    Hovertip(c1_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    cslabel2=ttk.Label(csLF, text = 'Enter Interest(Rate): ')
    cslabel2.grid(column=1,row=0)
    Hovertip(cslabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    c1_2 = ttk.Entry(csLF, textvariable=cs2)
    c1_2.grid(column=1, row=1)
    Hovertip(c1_2, 'Enter the Interest or Rate.', hover_delay=1000)

    cslabel3=ttk.Label(csLF, text = 'Enter Time: ')
    cslabel3.grid(column=2,row=0)
    Hovertip(cslabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    c1_3 = ttk.Entry(csLF, textvariable=cs3)
    c1_3.grid(column=2, row=1)
    Hovertip(c1_3, 'Enter the time or duration.', hover_delay=1000)

    cslabel4=ttk.Label(csLF, text = 'Enter Amount: ')
    cslabel4.grid(column=3,row=0)
    Hovertip(cslabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    c1_4 = ttk.Entry(csLF, textvariable=cs4)
    c1_4.grid(column=3, row=1)
    Hovertip(c1_4, 'Enter the amount.', hover_delay=1000)

    csAL = ttk.Label(csAF,text='Compound Interest: ')
    csAL.grid(column=0,row=0)

    cscb = ttk.Button(csBF,text='Clear',command=csClear)
    cscb.grid(column=0,row=0)
    csmb = ttk.Button(csBF,text='Show Answer',command=csAns)
    csmb.grid(column=1,row=0)
    csqb = ttk.Button(csBF,text='Quit',command=close_win)
    csqb.grid(column=2,row=0)

    #
    cplabel1=ttk.Label(cpLF, text = 'Enter Compound Interest: ')
    cplabel1.grid(column=0,row=0)
    Hovertip(cplabel1, 'Compound Interest is the total interest.', hover_delay=1000)
    c2_1 = ttk.Entry(cpLF, textvariable=cp1)
    c2_1.grid(column=0, row=1)
    Hovertip(c2_1, 'Enter the Compound Interest.', hover_delay=1000)

    cplabel2=ttk.Label(cpLF, text = 'Enter Interest(Rate): ')
    cplabel2.grid(column=1,row=0)
    Hovertip(cplabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    c2_2 = ttk.Entry(cpLF, textvariable=cp2)
    c2_2.grid(column=1, row=1)
    Hovertip(c2_2, 'Enter the Interest or Rate.', hover_delay=1000)

    cplabel3=ttk.Label(cpLF, text = 'Enter Time: ')
    cplabel3.grid(column=2,row=0)
    Hovertip(cplabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    c2_3 = ttk.Entry(cpLF, textvariable=cp3)
    c2_3.grid(column=2, row=1)
    Hovertip(c2_3, 'Enter the time or duration.', hover_delay=1000)

    cplabel4=ttk.Label(cpLF, text = 'Enter Amount: ')
    cplabel4.grid(column=3,row=0)
    Hovertip(cplabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    c2_4 = ttk.Entry(cpLF, textvariable=cp4)
    c2_4.grid(column=3, row=1)
    Hovertip(c2_4, 'Enter the amount.', hover_delay=1000)

    cpAL = ttk.Label(cpAF,text='Principle: ')
    cpAL.grid(column=0,row=0)

    cpcb = ttk.Button(cpBF,text='Clear',command=cpClear)
    cpcb.grid(column=0,row=0)
    cpmb = ttk.Button(cpBF,text='Show Answer',command=cpAns)
    cpmb.grid(column=1,row=0)
    cpqb = ttk.Button(cpBF,text='Quit',command=close_win)
    cpqb.grid(column=2,row=0)

    #
    cilabel1=ttk.Label(ciLF, text = 'Enter Principle: ')
    cilabel1.grid(column=0,row=0)
    Hovertip(cilabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    c3_1 = ttk.Entry(ciLF, textvariable=ci1)
    c3_1.grid(column=0, row=1)
    Hovertip(c3_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    cilabel2=ttk.Label(ciLF, text = 'Enter Compound Interest: ')
    cilabel2.grid(column=1,row=0)
    Hovertip(cilabel2, 'Compound Interest is the total interest.', hover_delay=1000)
    c3_2 = ttk.Entry(ciLF, textvariable=ci2)
    c3_2.grid(column=1, row=1)
    Hovertip(c3_2, 'Enter the Compound Interest.', hover_delay=1000)

    cilabel3=ttk.Label(ciLF, text = 'Enter Time: ')
    cilabel3.grid(column=2,row=0)
    Hovertip(cilabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    c3_3 = ttk.Entry(ciLF, textvariable=ci3)
    c3_3.grid(column=2, row=1)
    Hovertip(c3_3, 'Enter the time or duration.', hover_delay=1000)

    cilabel4=ttk.Label(ciLF, text = 'Enter Amount: ')
    cilabel4.grid(column=3,row=0)
    Hovertip(cilabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    c3_4 = ttk.Entry(ciLF, textvariable=ci4)
    c3_4.grid(column=3, row=1)
    Hovertip(c3_4, 'Enter the amount.', hover_delay=1000)

    ciAL = ttk.Label(ciAF,text='Interest: ')
    ciAL.grid(column=0,row=0)

    cicb = ttk.Button(ciBF,text='Clear',command=ciClear)
    cicb.grid(column=0,row=0)
    cimb = ttk.Button(ciBF,text='Show Answer',command=ciAns)
    cimb.grid(column=1,row=0)
    ciqb = ttk.Button(ciBF,text='Quit',command=close_win)
    ciqb.grid(column=2,row=0)

    #
    ctlabel1=ttk.Label(ctLF, text = 'Enter Principle: ')
    ctlabel1.grid(column=0,row=0)
    Hovertip(ctlabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    c4_1 = ttk.Entry(ctLF, textvariable=ct1)
    c4_1.grid(column=0, row=1)
    Hovertip(c4_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    ctlabel2=ttk.Label(ctLF, text = 'Enter Interest(Rate): ')
    ctlabel2.grid(column=1,row=0)
    Hovertip(ctlabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    c4_2 = ttk.Entry(ctLF, textvariable=ct2)
    c4_2.grid(column=1, row=1)
    Hovertip(c4_2, 'Enter the Interest or Rate.', hover_delay=1000)

    ctlabel3=ttk.Label(ctLF, text = 'Enter Compound Interest: ')
    ctlabel3.grid(column=2,row=0)
    Hovertip(ctlabel3, 'Compound Interest is the total interest.', hover_delay=1000)
    c4_3 = ttk.Entry(ctLF, textvariable=ct3)
    c4_3.grid(column=2, row=1)
    Hovertip(c4_3, 'Enter the Compound Interest.', hover_delay=1000)

    ctlabel4=ttk.Label(ctLF, text = 'Enter Amount: ')
    ctlabel4.grid(column=3,row=0)
    Hovertip(ctlabel4, 'Amount is the final increased version of the principle.', hover_delay=1000)
    c4_4 = ttk.Entry(ctLF, textvariable=ct4)
    c4_4.grid(column=3, row=1)
    Hovertip(c4_4, 'Enter the amount.', hover_delay=1000)

    ctAL = ttk.Label(ctAF,text='Time: ')
    ctAL.grid(column=0,row=0)

    ctcb = ttk.Button(ctBF,text='Clear',command=ctClear)
    ctcb.grid(column=0,row=0)
    ctmb = ttk.Button(ctBF,text='Show Answer',command=ctAns)
    ctmb.grid(column=1,row=0)
    ctqb = ttk.Button(ctBF,text='Quit',command=close_win)
    ctqb.grid(column=2,row=0)

    #
    calabel1=ttk.Label(caLF, text = 'Enter Principle: ')
    calabel1.grid(column=0,row=0)
    Hovertip(calabel1, 'Principle is the initial deposit or start amount.', hover_delay=1000)
    c5_1 = ttk.Entry(caLF, textvariable=ca1)
    c5_1.grid(column=0, row=1)
    Hovertip(c5_1, 'Enter the initial deposit or start amount.', hover_delay=1000)

    calabel2=ttk.Label(caLF, text = 'Enter Interest(Rate): ')
    calabel2.grid(column=1,row=0)
    Hovertip(calabel2, 'Interest is how much the principle increases in a given time.', hover_delay=1000)
    c5_2 = ttk.Entry(caLF, textvariable=ca2)
    c5_2.grid(column=1, row=1)
    Hovertip(c5_2, 'Enter the Interest or Rate.', hover_delay=1000)

    calabel3=ttk.Label(caLF, text = 'Enter Time: ')
    calabel3.grid(column=2,row=0)
    Hovertip(calabel3, 'Time is the duration of increase of princple.', hover_delay=1000)
    c5_3 = ttk.Entry(caLF, textvariable=ca3)
    c5_3.grid(column=2, row=1)
    Hovertip(c5_3, 'Enter the time or duration.', hover_delay=1000)

    calabel4=ttk.Label(caLF, text = 'Enter Compound Interest: ')
    calabel4.grid(column=3,row=0)
    Hovertip(calabel4, 'Compound Interest is the total interest.', hover_delay=1000)
    c5_4 = ttk.Entry(caLF, textvariable=ca4)
    c5_4.grid(column=3, row=1)
    Hovertip(c5_4, 'Enter the Compound Interest.', hover_delay=1000)

    caAL = ttk.Label(caAF,text='Amount: ')
    caAL.grid(column=0,row=0)

    cacb = ttk.Button(caBF,text='Clear',command=caClear)
    cacb.grid(column=0,row=0)
    camb = ttk.Button(caBF,text='Show Answer',command=caAns)
    camb.grid(column=1,row=0)
    caqb = ttk.Button(caBF,text='Quit',command=close_win)
    caqb.grid(column=2,row=0)

    cnb.grid(column=0,row=0)

    #
    cmbe(s1_1,s1_2,s1_3,s1_4,ssAns)
    cmbe(s2_1,s2_2,s2_3,s2_4,spAns)
    combo(s3_1,s3_2,s3_3,siAns)
    combo(s4_1,s4_2,s4_3,stAns)
    cmbe(s5_1,s5_2,s5_3,s5_4,saAns)

    cmbe(c1_1,c1_2,c1_3,c1_4,csAns)
    cmbe(c2_1,c2_2,c2_3,c2_4,cpAns)
    cmbe(c3_1,c3_2,c3_3,c3_4,ciAns)
    cmbe(c4_1,c4_2,c4_3,c4_4,ctAns)
    cmbe(c5_1,c5_2,c5_3,c5_4,caAns)

    win.bind('<Control-q>',shClose)

    nb.grid(column=0,row=0)
    s1_1.focus()
    win.config(menu = menubar)
    win.mainloop()

def ConvCalc():
    def reS(event):
        s1 = iov.get()
        s2 = oov.get()
        iov.set(s2)
        oov.set(s1)
        ie.focus()

    def mc(event):
        global io
        clicked = ov.get()
        if clicked == 'Length':
            io = [empty,'Nanometres','Micrometres (Microns)','Millimetres','Centimetres','Decimetres','Metres','Kilometres','Inches','Feet','Yards','Miles','Nautical Miles']
        elif clicked == 'Temperature':
            io = [empty,'Celsius','Farenheit','Kelvin']
        elif clicked == 'Weight and Mass':
            io = [empty,'Milligrams','Centigrams','Decigrams','Grams','Dekagrams','Hectograms','Kilograms','Tonnes','Newtons','Ounces','Stones','Pounds','Carats','Short tons (US)','Long tons (UK)']
        elif clicked == 'Time':
            io = [empty,'Microseconds','Milliseconds','Seconds','Minutes','Hours','Days','Weeks','Years']
        elif clicked == 'Volume':
            io = [empty,'Millilitres','Litres','Cubic Micrometres','Cubic Millimetres','Cubic Centimetres','Cubic Decimetres','Cubic Metres','Cubic Inches','Cubic Feet','Cubic Yards','Teaspoons(US)','Teaspoons(UK)','Tablespoons(US)','Tablespoons(UK)','Fluid Ounces(US)','Fluid Ounces(UK)','Cups(US)','Pints(US)','Pints(UK)','Quarts(US)','Quarts(UK)','Gallons(US)','Gallons(UK)']
        elif clicked == 'Energy':
            io = [empty,'Electron Volts','Joules','Kilojoules','Food Calories','Thermal Calories','Foot-Pounds','British Thermal Units']
        elif clicked == 'Area':
            io = [empty,'Square Millimetres','Square Centimetres','Square Decimetres','Square Metres','Square Kilometres','Hectares','Acres','Square Inches','Square Feet','Square Yards','Square Miles']
        elif clicked == 'Speed':
            io = [empty,'Millimetres per second','Centimetres per second','Metres per second','Kilometres per hour','Inches per second','Feet per second','Yards per second','Miles per hour','Knots','Mach']
        elif clicked == 'Power':
            io = [empty,'Watts','Kilowatts','Horsepower','Foot-Pounds/Minute','British Thermal Units/Minute']
        elif clicked == 'Pressure':
            io = [empty,'Pascals','Kilopascals','Atmospheres','Pounds/Square Inch','Bars','Millimetres of Mercury']
        elif clicked == 'Angle':
            io = [empty,'Degrees','Radians','Gradians']
        elif clicked == 'Computer Data':
            io = [empty,'Bits','Bytes','Kilobits','Kilobytes','Kibibits','Kibibytes','Megabits','Megabytes','Mebibits','Mebibytes','Gigabits','Gigabytes','Gibibits','Gibibytes','Terabits','Terabytes','Tebibits','Tebibytes','Petabits','Petabytes','Pebibits','Pebibytes','Exabits','Exabytes','Exbibits','Exbibytes','Zetabits','Zetabytes','Zebibits','Zebibytes','Yottabits','Yottabytes','Yobibits','Yobibytes']
        elif clicked == 'Number System':
            io = [empty,'Decimal','Binary','Hexadecimal','Octal']
        elif clicked == 'Frequency':
            io = [empty,'Hertz','Kilohertz','Megahertz','Gigahertz']
        elif clicked == 'Currency':
            io = [empty,'Rupee','Dollar','Euro','Pounds','Yen','Darhams']
        iu = ttk.OptionMenu(ccf, iov, *io)
        Hovertip(iu,'Select the unit of the input value.',hover_delay=500)
        iu.grid(column=0,row=1)
        ou = ttk.OptionMenu(ccf, oov, *io)
        Hovertip(ou,'Select the unit of the output value.',hover_delay=500)
        ou.grid(column=1,row=1)
        iov.set(io[1])
        oov.set(io[2])
        ie.focus()

    def hF():
        abl.configure(text='Help...')
        ie.focus()

    def aF():
        abl.configure(text='Conversion Calculator v1.4.1\nDevoloped and published by Jaiwanth Karthi')
        ie.focus()

    def ci():
        iv.set(empty)
        ansl.configure(text=empty)
        abl.configure(text=empty)
        ie.focus()

    def qmf(event):
        #remember()
        win.destroy()
        '''
        win.bell()
        mg = messagebox.askyesno(title='Close Window', message='Are you sure you want to quit the Conversion Calculator?')
        if mg == True:
            remember()
            win.destroy()
        else:
            pass
            ie.focus()
        '''

    def sa(event):
        try:
            clicked = ov.get()
            iop = iov.get()
            oop = oov.get()
            i = float(eval(ie.get()))
            if clicked == 'Length':
                hl = [1,1000000000,1000000,1000,100,10]
                hl2 = ['Metres','Nanometres','Micrometres (Microns)','Millimetres','Centimetres','Decimetres']
                hl3 = [1000,0.0254,0.3048,0.9144,1609.344,1852]
                hl4 = ['Kilometres','Inches','Feet','Yards','Miles','Nautical Miles']
                for icv in range(6):
                    if iop == hl2[icv]:
                        ao = i/(hl[icv])
                        if oop == 'Metres':
                            a = ao
                        elif oop == 'Feet':
                            a = ao/0.3048
                        elif oop == 'Inches':
                            a = ao/0.0254
                        elif oop == 'Yards':
                            a = ao/0.9144
                        elif oop == 'Miles':
                            a = ao/1609.344
                        elif oop == 'Nautical Miles':
                            a = ao/1852
                        elif oop == 'Nanometres':
                            a = ao*1000000000
                        elif oop == 'Micrometres (Microns)':
                            a = ao*1000000
                        elif oop == 'Kilometres':
                            a = ao/1000
                        elif oop == 'Millimetres':
                            a = ao*1000
                        elif oop == 'Centimetres':
                            a = ao*100
                        elif oop == 'Decimetres':
                            a = ao*10
                for icv in range(6):
                    if iop == hl4[icv]:
                        ao = i*(hl3[icv])
                        if oop == 'Metres':
                            a = ao
                        elif oop == 'Feet':
                            a = ao/0.3048
                        elif oop == 'Inches':
                            a = ao/0.0254
                        elif oop == 'Yards':
                            a = ao/0.9144
                        elif oop == 'Miles':
                            a = ao/1609.344
                        elif oop == 'Nautical Miles':
                            a = ao/1852
                        elif oop == 'Nanometres':
                            a = ao*1000000000
                        elif oop == 'Micrometres (Microns)':
                            a = ao*1000000
                        elif oop == 'Kilometres':
                            a = ao/1000
                        elif oop == 'Millimetres':
                            a = ao*1000
                        elif oop == 'Centimetres':
                            a = ao*100
                        elif oop == 'Decimetres':
                            a = ao*10
            elif clicked == 'Temperature':
                if iop == 'Celsius':
                    if oop == 'Celsius':
                        a = i
                    elif oop == 'Farenheit':
                        a = (9*i / 5) + 32
                    elif oop == 'Kelvin':
                        a = i + 273.15
                elif iop == 'Farenheit':
                    if oop == 'Celsius':
                        a = ((i-32)*5)/9
                    elif oop == 'Farenheit':
                        a = i
                    elif oop == 'Kelvin':
                        sv = (5*i - 160)/9
                        a = sv + 273.15
                elif iop == 'Kelvin':
                    if oop == 'Celsius':
                        a = i - 273.15
                    elif oop == 'Farenheit':
                        sv = i - 273.15
                        a = (9*sv + 160)/5
                    elif oop == 'Kelvin':
                        a = i
            elif clicked == 'Weight and Mass':
                hl = [1,1000,100,10,5,(9.8/1000)]
                hl2 = ['Grams','Milligrams','Centigrams','Decigrams','Carats','Newtons']
                hl3 = [10,100,1000,1000000,28.349523125,453.59237,6350.29318,907184.74,1016046.9088]
                hl4 = ['Dekagrams','Hectograms','Kilograms','Tonnes','Ounces','Pounds','Stones','Short tons (US)','Long tons (UK)']
                for icv in range(6):
                    if iop == hl2[icv]:
                        ao = i/(hl[icv])
                        if oop == 'Milligrams':
                            a = ao*1000
                        elif oop == 'Centigrams':
                            a = ao*100
                        elif oop == 'Decigrams':
                            a = ao*10
                        elif oop == 'Grams':
                            a = ao
                        elif oop == 'Dekagrams':
                            a = ao/10
                        elif oop == 'Hectograms':
                            a = ao/100
                        elif oop == 'Kilograms':
                            a = ao/1000
                        elif oop == 'Tonnes':
                            a = ao/1000000
                        elif oop == 'Newtons':
                            a = (ao/1000)*9.8
                        elif oop == 'Carats':
                            a = ao*5
                        elif oop == 'Ounces':
                            a = ao/28.349523125
                        elif oop == 'Pounds':
                            a = ao/453.59237
                        elif oop == 'Stones':
                            a = ao/6350.29318
                        elif oop == 'Short tons (US)':
                            a = ao/907184.74
                        elif oop == 'Long tons (UK)':
                            a = ao/1016046.9088
                for icv in range(9):
                    if iop == hl4[icv]:
                        ao = i*(hl3[icv])
                        if oop == 'Milligrams':
                            a = ao*1000
                        elif oop == 'Centigrams':
                            a = ao*100
                        elif oop == 'Decigrams':
                            a = ao*10
                        elif oop == 'Grams':
                            a = ao
                        elif oop == 'Dekagrams':
                            a = ao/10
                        elif oop == 'Hectograms':
                            a = ao/100
                        elif oop == 'Kilograms':
                            a = ao/1000
                        elif oop == 'Tonnes':
                            a = ao/1000000
                        elif oop == 'Newtons':
                            a = (ao/1000)*9.8
                        elif oop == 'Carats':
                            a = ao*5
                        elif oop == 'Ounces':
                            a = ao/28.349523125
                        elif oop == 'Pounds':
                            a = ao/453.59237
                        elif oop == 'Stones':
                            a = ao/6350.29318
                        elif oop == 'Short tons (US)':
                            a = ao/907184.74
                        elif oop == 'Long tons (UK)':
                            a = ao/1016046.9088
            elif clicked == 'Time':
                hl = [1,1000,1000000]
                hl2 = ['Seconds','Milliseconds','Microseconds']
                hl3 = [60,3600,86400,604800,31557600]
                hl4 = ['Minutes','Hours','Days','Weeks','Years']
                for icv in range(3):
                    if iop == hl2[icv]:
                        ao = i/hl[icv]
                        if oop == 'Seconds':
                            a = ao
                        elif oop == 'Minutes':
                            a = ao/60
                        elif oop == 'Hours':
                            a = ao/3600
                        elif oop == 'Microseconds':
                            a = ao*1000000
                        elif oop == 'Milliseconds':
                            a = ao*1000
                        elif oop == 'Days':
                            a = ao/86400
                        elif oop == 'Weeks':
                            a = ao/604800
                        elif oop == 'Years':
                            a = ao/31557600
                for icv in range(5):
                    if iop == hl4[icv]:
                        ao = i*hl3[icv]
                        if oop == 'Seconds':
                            a = ao
                        elif oop == 'Minutes':
                            a = ao/60
                        elif oop == 'Hours':
                            a = ao/3600
                        elif oop == 'Microseconds':
                            a = ao*1000000
                        elif oop == 'Milliseconds':
                            a = ao*1000
                        elif oop == 'Days':
                            a = ao/86400
                        elif oop == 'Weeks':
                            a = ao/604800
                        elif oop == 'Years':
                            a = ao/31557600
            elif clicked == 'Computer Data':
                al1=['Bits','Kilobits', 'Megabits', 'Gigabits', 'Terabits', 'Petabits', 'Exabits', 'Zetabits', 'Yottabits']
                al2=['Bytes','Kilobytes', 'Megabytes', 'Gigabytes', 'Terabytes', 'Petabytes', 'Exabytes', 'Zetabytes', 'Yottabytes']
                al3=[empty,'Kibibits', 'Mebibits', 'Gibibits', 'Tebibits', 'Pebibits', 'Exbibits', 'Zebibits', 'Yobibits']
                al4=[empty,'Kibibytes', 'Mebibytes', 'Gibibytes', 'Tebibytes', 'Pebibytes', 'Exbibytes', 'Zebibytes', 'Yobibytes']
                l3 = [[al1,al2],[al3,al4]]
                for r in range(len(al1)):
                    for j in l3:
                        for q in j:
                            if iop == q[r]:
                                for g in range(len(al1)):
                                    for p in l3:
                                        for s in p:
                                            if oop == s[g]:
                                                v = r-g
                                                v1 = 1000**v
                                                v2 = 1024**v
                                                v3 = 1000**(r)
                                                v4 = 1024**(r)
                                                fv3 = (i*v3)/v4
                                                fv4 = (i*v4)/v3
                                                if q == l3[0][0]:
                                                    if s == l3[0][0]:
                                                        a = i*v1
                                                    elif s == l3[0][1]:
                                                        a = (i*v1)/8
                                                    elif s == l3[1][0]:
                                                        a = fv3
                                                    elif s == l3[1][1]:
                                                        a = fv3/8
                                                elif q == l3[0][1]:
                                                    if s == l3[0][0]:
                                                        a = (i*v1)*8
                                                    elif s == l3[0][1]:
                                                        a = i*v1
                                                    elif s == l3[1][0]:
                                                        a = fv3*8
                                                    elif s == l3[1][1]:
                                                        a = fv3
                                                elif q == l3[1][0]:
                                                    if s == l3[0][0]:
                                                        a = fv4
                                                    elif s == l3[0][1]:
                                                        a = fv4/8
                                                    elif s == l3[1][0]:
                                                        a = i*v2
                                                    elif s == l3[1][1]:
                                                        a = (i*v2)/8
                                                elif q == l3[1][1]:
                                                    if s == l3[0][0]:
                                                        a = fv4*8
                                                    elif s == l3[0][1]:
                                                        a = fv4
                                                    elif s == l3[1][0]:
                                                        a = (i*v2)*8
                                                    elif s == l3[1][1]:
                                                        a = i*v2
            elif clicked == 'Number System':
                if iop == 'Decimal':
                    if oop == 'Decimal':
                        a = i
                    elif oop == 'Binary':
                        if i!=0:
                            c=1
                            s = ''
                            ai = int(i)
                            while ai!=1:
                                r = str(ai%2)
                                ai = int(ai/2)
                                s = str(int(r))+s
                            a = int('1'+s)  
                        else:
                            a=0
                elif iop == 'Binary':
                    if oop == 'Decimal':
                        ai=str(int(i))
                        c=len(ai)
                        s = ''
                        d=0
                        for j in ai:
                            c=c-1
                            f = (2**c)*int(j)
                            s=s+str(f)
                        for l in s:
                            d=d+int(l)
                        a = d
                    elif oop == 'Binary':
                        a = i
                elif iop == 'Octal':
                    if oop == 'Octal':
                        a = i
                elif iop == 'Hexadecimal':
                    if oop == 'Hexadecimal':
                        a = i
            elif clicked == 'Angle':
                pir = math.pi/180
                if iop == 'Degrees':
                    if oop == 'Degrees':
                        a = i
                    elif oop == 'Radians':
                        a = i*pir
                    elif oop == 'Gradians':
                        a = i*(10/9)
                elif iop == 'Radians':
                    if oop == 'Degrees':
                        a = i/pir
                    elif oop == 'Radians':
                        a = i
                    elif oop == 'Gradians':
                        a = (i/pir)*(10/9)
            elif clicked == 'Frequency':
                hl = [1,1000,1000000,1000000000]
                hl2 = ['Hertz','Kilohertz','Megahertz','Gigahertz']
                for icv in range(4):
                    if iop == hl2[icv]:
                        ao = i*hl[icv]
                        if oop == 'Hertz':
                            a = ao
                        elif oop == 'Kilohertz':
                            a = ao/1000
                        elif oop == 'Megahertz':
                            a = ao/1000000
                        elif oop == 'Gigahertz':
                            a = ao/1000000000
            elif clicked == 'Pressure':
                if iop == 'Pascals':
                    if oop == 'Pascals':
                        a = i
                    elif oop == 'Kilopascals':
                        a = i/1000
                    elif oop == 'Atmospheres':
                        a = i/101325
                    elif oop == 'Bars':
                        a = i/100000
                    elif oop == 'Pounds/Square Inch':
                        a = i/6894.757
                    elif oop == 'Millimetres of Mercury':
                        a = i/133.3
                elif iop == 'Kilopascals':
                    if oop == 'Pascals':
                        a = i*1000
                    elif oop == 'Kilopascals':
                        a = i
                    elif oop == 'Atmospheres':
                        a = i/101.325
                    elif oop == 'Bars':
                        a = i/100
                    elif oop == 'Pounds/Square Inch':
                        a = i/6.894757
                    elif oop == 'Millimetres of Mercury':
                        a = i*7.501875
                elif iop == 'Atmospheres':
                    if oop == 'Pascals':
                        a = i*101325
                    elif oop == 'Kilopascals':
                        a = i*101.325
                    elif oop == 'Atmospheres':
                        a = i
                    elif oop == 'Bars':
                        a = i*1.01325
                    elif oop == 'Pounds/Square Inch':
                        a = i*14.6959494003922
                    elif oop == 'Millimetres of Mercury':
                        a = i*760.1275
                elif iop == 'Bars':
                    if oop == 'Pascals':
                        a = i*100000
                    elif oop == 'Kilopascals':
                        a = i*100
                    elif oop == 'Atmospheres':
                        a = i/1.01325
                    elif oop == 'Bars':
                        a = i
                    elif oop == 'Pounds/Square Inch':
                        a = i*14.50377
                    elif oop == 'Millimetres of Mercury':
                        a = i*750.1875
                elif iop == 'Pounds/Square Inch':
                    if oop == 'Pascals':
                        a = i*6894.757
                    elif oop == 'Kilopascals':
                        a = i*6.894757
                    elif oop == 'Atmospheres':
                        a = i/14.6959494003922
                    elif oop == 'Bars':
                        a = i/14.50377
                    elif oop == 'Pounds/Square Inch':
                        a = i
                    elif oop == 'Millimetres of Mercury':
                        a = i*51.7236084021023
                elif iop == 'Millimetres of Mercury':
                    if oop == 'Pascals':
                        a = i*133.3
                    elif oop == 'Kilopascals':
                        a = i/7.501875
                    elif oop == 'Atmospheres':
                        a = i/760.1275
                    elif oop == 'Bars':
                        a = i/750.1875
                    elif oop == 'Pounds/Square Inch':
                        a = i/51.7236084021023
                    elif oop == 'Millimetres of Mercury':
                        a = i 
            elif clicked == 'Power':
                if iop == 'Watts':
                    if oop == 'Watts':
                        a = i
                    elif oop == 'Kilowatts':
                        a = i/1000
                    elif oop == 'Horsepower':
                        a = i/745.699871582270
                    elif oop == 'Foot-pounds/Minute':
                        a = i*44.2537289566360
                    elif oop == 'British Thermal Units/Minute':
                        a = i/(160.584/9)
                elif iop == 'Kilowatts':
                    if oop == 'Watts':
                        a = i*1000
                    elif oop == 'Kilowatts':
                        a = i
                    elif oop == 'Horsepower':
                        a = i/0.745699871582270
                    elif oop == 'Foot-pounds/Minute':
                        a = i*44253.7289566360
                    elif oop == 'British Thermal Units/Minute':
                        a = (i/(160.584/9))/1000
                elif iop == 'Horsepower':
                    if oop == 'Watts':
                        a = i*745.699871582270
                    elif oop == 'Kilowatts':
                        a = i*0.745699871582270
                    elif oop == 'Horsepower':
                        a = i
                    elif oop == 'Foot-pounds/Minute':
                        a = i*33000
                    elif oop == 'British Thermal Units/Minute':
                        a = i*42.4072203702327
                elif iop == 'Foot-pounds/Minute':
                    if oop == 'Watts':
                        a = i/44.2537289566360
                    elif oop == 'Kilowatts':
                        a = i*44253.7289566360
                    elif oop == 'Horsepower':
                        a = i/33000
                    elif oop == 'Foot-pounds/Minute':
                        a = i
                    elif oop == 'British Thermal Units/Minute':
                        a = i/778.169370967876
            elif clicked == 'Area': 
                hl = [1,1000000,10000,100,1550.0031000062017,10.763910416709699,1.195990046301085,0.00000038610215854244587]
                hl2 = ['Square Metres','Square Millimetres','Square Centimetres','Square Decimetres','Square Inches','Square Feet','Square Yards','Square Miles']
                hl3 = [1000000,10000,4046.8564224]
                hl4 = ['Square Kilometres','Hectares','Acres']
                for icv in range(8):
                    if iop == hl2[icv]:
                        ao = i/(hl[icv])
                        if oop == 'Square Metres':
                            a = ao
                        elif oop == 'Square Millimetres':
                            a = ao*1000000
                        elif oop == 'Square Centimetres':
                            a = ao*10000
                        elif oop == 'Square Decimetres':
                            a = ao*100
                        elif oop == 'Square Kilometres':
                            a = ao/1000000
                        elif oop == 'Square Inches':
                            a = ao*1550.0031000062017
                        elif oop == 'Square Feet':
                            a = ao*10.763910416709699
                        elif oop == 'Square Miles':
                            a = ao*0.00000038610215854244587
                        elif oop == 'Square Yards':
                            a = ao*1.195990046301085
                        elif oop == 'Hectares':
                            a = ao/10000
                        elif oop == 'Acres':
                            a = ao/4046.8564224
                for icv in range(3):
                    if iop == hl4[icv]:
                        ao = i*(hl3[icv])
                        if oop == 'Square Metres':
                            a = ao
                        elif oop == 'Square Millimetres':
                            a = ao*1000000
                        elif oop == 'Square Centimetres':
                            a = ao*10000
                        elif oop == 'Square Decimetres':
                            a = ao*100
                        elif oop == 'Square Kilometres':
                            a = ao/1000000
                        elif oop == 'Square Inches':
                            a = ao*1550.0031000062017
                        elif oop == 'Square Feet':
                            a = ao*10.763910416709699
                        elif oop == 'Square Miles':
                            a = ao*0.00000038610215854244587
                        elif oop == 'Square Yards':
                            a = ao*1.195990046301085
                        elif oop == 'Hectares':
                            a = ao/10000
                        elif oop == 'Acres':
                            a = ao/4046.8564224
            elif clicked == 'Energy':
                hl = [1000,4.184,4184,1.3558179483314,1055.056]
                hl2 = ['Kilojoules','Thermal Calories','Food Calories','Foot-Pounds','British Thermal Units']
                hl3 = [1,6.24150934326018e+18]
                hl4 = ['Joules','Electron Volts']
                for icv in range(5):
                    if iop == hl2[icv]:
                        ao = hl[icv]
                        if oop == 'Joules':
                            a = ao
                        elif oop == 'Kilojoules':
                            a = ao/1000
                        elif oop == 'Electron Volts':
                            a = ao*6.24150934326018e+18
                        elif oop == 'Thermal Calories':
                            a = ao/4.184
                        elif oop == 'Food Calories':
                            a = ao/4184
                        elif oop == 'Foot-Pounds':
                            a = ao/1.3558179483314
                        elif oop == 'British Thermal Units':
                            a = ao/1055.056
                for icv in range(2):
                    if iop == hl4[icv]:
                        ao = hl3[icv]
                        if oop == 'Joules':
                            a = ao
                        elif oop == 'Kilojoules':
                            a = ao/1000
                        elif oop == 'Electron Volts':
                            a = ao*6.24150934326018e+18
                        elif oop == 'Thermal Calories':
                            a = ao/4.184
                        elif oop == 'Food Calories':
                            a = ao/4184
                        elif oop == 'Foot-Pounds':
                            a = ao/1.3558179483314
                        elif oop == 'British Thermal Units':
                            a = ao/1055.056
            elif clicked == 'Speed':
                hl = [1000,100,1,3.6]
                hl2 = ['Millimetres per second','Centimetres per second','Metres per second','Kilometres per hour']
                hl3 = [0.0254,0.3048,0.9144,0.447,0.5144,340.3]
                hl4 = ['Inches per second','Feet per second','Yards per second','Miles per hour','Knots','Mach']
                for icv in range(4):
                    if iop == hl2[icv]:
                        ao = i/hl[icv]
                        if oop == 'Metres per second':
                            a = ao
                        elif oop == 'Centimetres per second':
                            a = ao*100
                        elif oop == 'Millimetres per second':
                            a = ao*1000
                        elif oop == 'Kilometres per hour':
                            a = ao*3.6
                        elif oop == 'Feet per second':
                            a = ao/0.3048
                        elif oop == 'Inches per second':
                            a = ao/0.0254
                        elif oop == 'Yards per second':
                            a = ao/0.9144
                        elif oop == 'Miles per hour':
                            a = ao/0.447
                        elif oop == 'Mach':
                            a = ao/340.3
                        elif oop == 'Knots':
                            a = ao/0.5144
                for icv in range(6):
                    if iop == hl4[icv]:
                        ao = i*hl3[icv]
                        if oop == 'Metres per second':
                            a = ao
                        elif oop == 'Centimetres per second':
                            a = ao*100
                        elif oop == 'Millimetres per second':
                            a = ao*1000
                        elif oop == 'Kilometres per hour':
                            a = ao*3.6
                        elif oop == 'Feet per second':
                            a = ao/0.3048
                        elif oop == 'Inches per second':
                            a = ao/0.0254
                        elif oop == 'Yards per second':
                            a = ao/0.9144
                        elif oop == 'Miles per hour':
                            a = ao/0.447
                        elif oop == 'Mach':
                            a = ao/340.3
                        elif oop == 'Knots':
                            a = ao/0.5144
            elif clicked == 'Volume':
                sc = 4.92892159375
                kc = 5.9193880208+((1/30000000000))
                hl = [1,1000,(1/1000_0000_0000),(1/1000),1,1000,1000_000,16.387064,28316.846592,764554.857984,sc,kc,(sc*3),(kc*3),(sc*6),(kc*4.8),(sc*48),(sc*96),(kc*96),(sc*192),(kc*192),(sc*768),(kc*768)]
                hl2 = ['Millilitres','Litres','Cubic Micrometres','Cubic Millimetres','Cubic Centimetres','Cubic Decimetres','Cubic Metres','Cubic Inches','Cubic Feet','Cubic Yards','Teaspoons(US)','Teaspoons(UK)','Tablespoons(US)','Tablespoons(UK)','Fluid Ounces(US)','Fluid Ounces(UK)','Cups(US)','Pints(US)','Pints(UK)','Quarts(US)','Quarts(UK)','Gallons(US)','Gallons(UK)']
                for icv in range(23):
                    if iop == hl2[icv]:
                        ao = i*(hl[icv])
                        usc = ao/sc
                        ukc = ao/kc
                        if oop == 'Millilitres':
                            a = ao
                        elif oop == 'Litres':
                            a = ao/1000
                        elif oop == 'Cubic Centimetres':
                            a = ao
                        elif oop == 'Cubic Decimetres':
                            a = ao/1000
                        elif oop == 'Cubic Metres':
                            a = ao/1000_000
                        elif oop == 'Cubic Millimetres':
                            a = ao*1000
                        elif oop == 'Cubic Micrometres':
                            a = ao*1000_0000_0000
                        elif oop == 'Cubic Inches':
                            a = ao/16.387064
                        elif oop == 'Cubic Feet':
                            a = ao/28316.846592
                        elif oop == 'Cubic Yards':
                            a = ao/764554.857984
                        elif oop == 'Teaspoons(US)':
                            a = usc
                        elif oop == 'Tablespoons(US)':
                            a = usc/3
                        elif oop == 'Fluid Ounces(US)':
                            a = usc/6
                        elif oop == 'Cups(US)':
                            a = usc/48
                        elif oop == 'Pints(US)':
                            a = usc/96
                        elif oop == 'Quarts(US)':
                            a = usc/192
                        elif oop == 'Gallons(US)':
                            a = usc/768
                        elif oop == 'Teaspoons(UK)':
                            a = ukc
                        elif oop == 'Tablespoons(UK)':
                            a = ukc/3
                        elif oop == 'Fluid Ounces(UK)':
                            a = ukc/4.8
                        elif oop == 'Pints(UK)':
                            a = ukc/96
                        elif oop == 'Quarts(UK)':
                            a = ukc/192
                        elif oop == 'Gallons(UK)':
                            a = ukc/768
            elif clicked == 'Currency':pass
            if dv.get() == 'Decimal':
                pass
            elif dv.get() == 'Fraction':
                a = Fraction(a)

            if oop == 'British Thermal Units':
                ansl.configure(text='BTUs: ' + str(a))
            elif oop == 'British Thermal Units/Minute':
                ansl.configure(text='BTUs/Minute: ' + str(a))
            elif oop == 'Millimetres of Mercury':
                ansl.configure(text='mmHg: ' + str(a))
            else:
                ansl.configure(text=str(oop) + ': ' + str(a))
            ie.focus()
        except ValueError or  _tkinter.TclError:
            pass
        except UnboundLocalError:
            pass

    def remember():
        o1 = ov.get()
        o2 = iov.get()
        o3 = oov.get()
        with open('entrydat.pkl','wb') as f:
            pkl.dump(o1,f)
            pkl.dump(o2,f)
            pkl.dump(o3,f)

    def recollect():
        try:
            with open('entrydat.pkl','rb') as f:
                o1 = pkl.load(f)
                o2 = pkl.load(f)
                o3 = pkl.load(f)
                ov.set(o1)
                iov.set(o2)
                oov.set(o3)
            ie.focus()
        except:
            pass

    def iefoc(event):
        ie.focus()

    empty = ' '
    win = tk.Toplevel(root)
    win.title('Conversion Calculator')
    menubar = tk.Menu(win)
    helpmenu = tk.Menu(menubar, tearoff=1)
    helpmenu.add_command(label='Help', command=hF)
    helpmenu.add_command(label='About', command=aF)
    menubar.add_cascade(label='Help', menu=helpmenu)

    mf = ttk.LabelFrame(win,height=100,width=50)
    mf.grid(column=0,row=0,padx=15)
    inpf = ttk.Frame(mf)
    inpf.grid(column=0,row=0,pady=5)
    bf = ttk.Frame(mf)
    bf.grid(column=0,row=1,pady=5)
    af = ttk.Frame(mf)
    af.grid(column=0,row=2,pady=5)
    abf = ttk.Frame(mf)
    abf.grid(column=0,row=3,pady=2)
    cf = ttk.LabelFrame(win,height=100,width=50)
    cf.grid(column=1,row=0,padx=15)
    ucf = ttk.Frame(cf)
    ucf.grid(column=0,row=0,pady=5)
    ccf = ttk.Frame(cf)
    ccf.grid(column=0,row=1,pady=15)
    rbcf = ttk.Frame(cf)
    rbcf.grid(column=0,row=2,pady=0)

    askl = ttk.Label(inpf,text='Enter Input Value:')
    askl.grid(column=0,row=0)
    Hovertip(askl,'Input value is the value that should be converted.',hover_delay=750)
    iv=tk.DoubleVar()
    iv.set(empty)
    ie = ttk.Entry(inpf,textvariable=iv)
    Hovertip(ie,'Enter the input value.',hover_delay=500)
    ie.bind('<Return>',sa)
    ie.bind('<Alt-a>',sa)
    win.bind('<Alt-a>',sa)
    ie.bind('<Alt-r>',reS)
    ie.grid(column=0,row=1)
    cb = ttk.Button(bf,text='Clear',command=ci)
    Hovertip(cb,'Clear all the data in the answer space, help space and entry space.',hover_delay=500)
    cb.grid(column=0,row=0)
    ab = ttk.Button(bf,text='Show Answer',command=lambda:sa(None))
    Hovertip(ab,'Show the conversion of the input value to the selected output unit.',hover_delay=500)
    ab.grid(column=1,row=0)
    dfl=[empty,'Decimal','Fraction']
    dv = tk.StringVar()
    dfb = ttk.OptionMenu(bf,dv,*dfl,command=iefoc)
    dfb.grid(column=2,row=0)
    dv.set(dfl[1])
    ansl = ttk.Label(af,text='')
    ansl.grid(column=0,row=0)
    abl = ttk.Label(abf,text='')
    abl.grid(column=0,row=0)

    options = ["Choose Conversion Measure","Length","Temperature","Weight and Mass","Time","Volume","Area","Speed","Angle","Power","Pressure","Energy",'Frequency',"Computer Data",'Number System',"Currency"]
    ov = tk.StringVar()
    iov = tk.StringVar()
    oov = tk.StringVar()
    us = ttk.OptionMenu(ucf, ov, *options, command=mc)
    Hovertip(us,'Select the main measure in which conversion occurs.',hover_delay=500)
    us.grid(column=1,row=0,columnspan=2)
    ov.set(options[1])
    dl1 = tk.Label(ucf,text='Select Conversion Measure:')
    Hovertip(dl1,'Conversion measure is the main measure in which the conversion of values according to units occur.',hover_delay=750)
    dl1.grid(column=0,row=0)
    dl2 = ttk.Label(ccf,text='Select Input Unit:')
    Hovertip(dl2,'Input unit is the unit of the input value.',hover_delay=750)
    dl2.grid(column=0,row=0)
    dl3 = ttk.Label(ccf,text='Select Output Unit:')
    Hovertip(dl3,'Output unit is the unit of the output value.',hover_delay=750)
    dl3.grid(column=1,row=0)
    swapb = ttk.Button(rbcf,text='Reverse unit selections',command=lambda:reS(None))
    Hovertip(cb,'Swap the selected units.',hover_delay=300)
    swapb.grid(column=0,row=2,columnspan=2)
    mc(None)
    recollect()

    win.config(menu=menubar)
    win.focus()
    ie.focus()
    win.bind('<Control-q>',qmf)
    win.protocol('WM_DELETE_WINDOW',lambda:qmf(None))
    win.mainloop()

def ntbk():
    pass


def run_hexon():
    global root, empty
    
    root = tk.Tk()
    root.title('The Calculator Hexon')
    menu = tk.Menu(root)
    emp = ''
    empty = ' '

    helpmenu = tk.Menu(menu, tearoff=1)
    helpmenu.add_command(label='About', command=mainAbout)
    menu.add_cascade(label='Help', menu=helpmenu)

    f = ttk.Labelframe(root,text='Other Options')
    f.grid(column=0,row=4)
    el1 = tk.Label(root,text='')
    el1.grid(column=0,row=3)
    el2 = tk.Label(root,text='')
    el2.grid(column=0,row=5)
    fm = ttk.Labelframe(root,text='Calculators')
    fm.grid(column=0,row=2)

    el0 = ttk.Label(root,text=' ')
    el0.grid(column=0,row=1)

    wl = tk.Label(root,bg='light grey',font='Calibri 20 bold italic',width='25',text="The Calculator Hexon")
    wl.grid(column=0,row=0)

    #ntb = ttk.Button(f,text="The NoteTaker",command = ntbk)
    #ntb.grid(column=0,row=0)
    #Hovertip(ntb,'Open the NoteTaker, an note-making and storing extension.',hover_delay=700)

    m1 = ttk.Menubutton(fm, text='Normal Calculators')
    m1.menu = tk.Menu(m1,tearoff=False)
    m1['menu'] = m1.menu
    m1.menu.add_command(label='Standard',command=Calc_init)
    m1.grid(column=0,row=0)

    m2 = ttk.Menubutton(fm, text='Sequencers and Graphers')
    m2.menu = tk.Menu(m2,tearoff=False)
    m2['menu'] = m2.menu
    m2.menu.add_command(label='Arithmetic Sequence Rule Finder',command=Arithmetic_calc_init)
    m2.menu.add_command(label='Geometric Sequence Rule Finder',command=Geo_Calc_init)
    m2.grid(column=0,row=1)

    m3 = ttk.Menubutton(fm, text='Objective Calculators')
    m3.menu = tk.Menu(m3,tearoff=False)
    m3['menu'] = m3.menu
    m3.menu.add_command(label='Unit Conversion',command=ConvCalc)
    m3.menu.add_command(label='Simple and Compound Interest',command=iCalc_init)
    m3.grid(column=1,row=0)

    root.protocol('WM_DELETE_WINDOW',lambda:smClose(None))
    root.bind('<Control-q>',smClose)
    m1.focus()
    root.config(menu=menu)
    root.mainloop()
