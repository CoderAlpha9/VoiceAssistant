from vpython import box, vector, color, canvas, hat
from tkinter import Tk, Button, Menu, Canvas, Scrollbar, StringVar, BOTH, YES, messagebox, filedialog, ttk, colorchooser, \
simpledialog
from random import choice
from math import sin, cos, asin, acos, pi, degrees, radians


class phantomObject():
    def __init__(self, pos):
        self.pos = pos
        self.size = vector(0, 0, 0)
        self.color = vector(0, 0, 0)

    def rotate(self, **k):
        pass


s, ss, ms, ds, pl, undoList, redoList = 0, 0, 0, 0, [], [], []
win, alg, solveBtn, undoBtn, redoBtn, cefl, cecl, cerl, ceccl, ce1b, ce2b, cepb, cenb = None, None, None, None, None, None, None, None, None, None, None, None, None
ceClr, ceFace, ceClmn, ceRow, ceList = None, 1, 1, 1, [None, 'Front', 'Top', 'Left', 'Down', 'Right', 'Back']
reverseColors = {'<1, 1, 1>':'White','<1, 0, 0>':'Red','<0, 1, 0>':'Green','<0, 0, 1>':'Blue','<1, 0.6, 0>':'Orange','<1, 1, 0>':'Yellow'}
cnvs = canvas(height=500, width=500, background=color.black)

# (("R","L","U","D","F","B","M","E","S","X","Y","Z"),("R","R'","L","L'","U","U'","D","D'","F","F'","B","B'","M","M'","E","E'","S","S'","X","X'","Y","Y'","Z","Z'"),("r","l","u","d","f","b","m","e","s"),("r","r'","l","l'","u","u'","d","d'","f","f'","b","b'","m","m'","e","e'","s","s'"))
cmndLib = {
    "R": "Rn(0,1,2)", "R'": "Rn(0,-1,2)", "L": "Ln(0,1,2)", "L'": "Ln(0,-1,2)",
    "U": "Un(0,1,2)", "U'": "Un(0,-1,2)", "D": "Dn(0,1,2)", "D'": "Dn(0,-1,2)",
    "F": "Fn(0,1,2)", "F'": "Fn(0,-1,2)", "B": "Bn(0,1,2)", "B'": "Bn(0,-1,2)",
    "X": "Ln(0,-1,s)", "X'": "Ln(0,1,s)", "Y": "Dn(0,-1,s)", "Y'": "Dn(0,1,s)", "Z": "Bn(0,-1,s)", "Z'": "Bn(0,1,s)",
    "r": "Rn(0,1,ds+2)", "r'": "Rn(0,-1,ds+2)", "l": "Ln(0,1,ds+2)", "l'": "Ln(0,-1,ds+2)",
    "u": "Un(0,1,ds+2)", "u'": "Un(0,-1,ds+2)", "d": "Dn(0,1,ds+2)", "d'": "Dn(0,-1,ds+2)",
    "f": "Fn(0,1,ds+2)", "f'": "Fn(0,-1,ds+2)", "b": "Bn(0,1,ds+2)", "b'": "Bn(0,-1,ds+2)"}


def setPlace():
    for x in range(s):
        for y in range(s):
            for z in range(s):
                rp = pl[x][y][z]
                tp = pl[round(rp.pos.x)][round(rp.pos.y)][round(rp.pos.z)]
                pl[x][y][z] = tp
                pl[round(rp.pos.x)][round(rp.pos.y)][round(rp.pos.z)] = rp
                tp.pos = vector(x, y, z)

                if z == 0:
                    pl[x][y][z].pos.z = pl[x][y][z].pos.z + 0.4995
                elif z == ss:
                    pl[x][y][z].pos.z = pl[x][y][z].pos.z - 0.4995
                elif y == 0:
                    pl[x][y][z].pos.y = pl[x][y][z].pos.y + 0.4995
                elif y == ss:
                    pl[x][y][z].pos.y = pl[x][y][z].pos.y - 0.4995
                elif x == 0:
                    pl[x][y][z].pos.x = pl[x][y][z].pos.x + 0.4995
                else:
                    pl[x][y][z].pos.x = pl[x][y][z].pos.x - 0.4995


def Rn(r, t=1, n=1, ue=True):
    updateUndo('Rn', r, t, n, ue)
    n = s - n
    r = s - r
    for x in range(n, r):
        for y in range(s):
            for z in range(s):
                pl[x][y][z].rotate(angle=t * -pi / 2, axis=vector(1, 0, 0), origin=vector(n, ss / 2, ss / 2))
    setPlace()


def Ln(n, t=1, r=1, ue=True):
    updateUndo('Ln', n, t, r, ue)
    for x in range(n, r):
        for y in range(s):
            for z in range(s):
                pl[x][y][z].rotate(angle=t * pi / 2, axis=vector(1, 0, 0), origin=vector(n, ss / 2, ss / 2))
    setPlace()


def Un(r, t=1, n=1, ue=True):
    updateUndo('Un', r, t, n, ue)
    n = s - n
    r = s - r
    for x in range(s):
        for y in range(n, r):
            for z in range(s):
                pl[x][y][z].rotate(angle=t * -pi / 2, axis=vector(0, 1, 0), origin=vector(ss / 2, n, ss / 2))
    setPlace()


def Dn(n, t=1, r=1, ue=True):
    updateUndo('Dn', n, t, r, ue)
    for x in range(s):
        for y in range(n, r):
            for z in range(s):
                pl[x][y][z].rotate(angle=t * pi / 2, axis=vector(0, 1, 0), origin=vector(ss / 2, n, ss / 2))
    setPlace()


def Fn(r, t=1, n=1, ue=True):
    updateUndo('Fn', r, t, n, ue)
    n = s - n
    r = s - r
    for x in range(s):
        for y in range(s):
            for z in range(n, r):
                pl[x][y][z].rotate(angle=t * -pi / 2, axis=vector(0, 0, 1), origin=vector(ss / 2, ss / 2, n))
    setPlace()


def Bn(n, t=1, r=1, ue=True):
    updateUndo('Bn', n, t, r, ue)
    for x in range(s):
        for y in range(s):
            for z in range(n, r):
                pl[x][y][z].rotate(angle=t * pi / 2, axis=vector(0, 0, 1), origin=vector(ss / 2, ss / 2, n))
    setPlace()


def reset():
    global undoList, redoList
    for x in range(s):
        for y in range(s):
            for z in range(s):
                if z == 0:
                    pl[x][y][z].color = color.yellow
                elif z == ss:
                    pl[x][y][z].color = color.white
                elif y == 0:
                    pl[x][y][z].color = color.orange
                elif y == ss:
                    pl[x][y][z].color = color.red
                elif x == 0:
                    pl[x][y][z].color = color.blue
                elif x == ss:
                    pl[x][y][z].color = color.green
    setPlace()
    redoBtn.configure(state='disabled')
    undoBtn.configure(state='disabled')
    undoList, redoList = [], []


def changeCnvsClr():
    cClr = colorchooser.askcolor(title='Choose Background Colour')
    cnvs.background = hat(vector(cClr[0][0], cClr[0][1], cClr[0][2]))


def updateCubeType(cubeType):
    win.destroy()
    destroyVisuals()
    vCube(int(cubeType))


def destroyVisuals():
    global pl
    for x in range(s):
        for y in range(s):
            for z in range(s):
                pl[0][0][0].visible = False
                del (pl[0][0][0])
            del (pl[0][0])
        del (pl[0])
    pl = []


def saveCube():
    pcl = []
    for x in range(s):
        pcl.append([])
        for y in range(s):
            pcl[x].append([])
            for z in range(s):
                pcl[x][y].append((pl[x][y][z].color.x, pl[x][y][z].color.y, pl[x][y][z].color.z))
    f = filedialog.asksaveasfile(mode='w', defaultextension=".cube")
    if f is None:
        return
    f.write(f'{pcl}')
    f.close()


def openCube():
    global s, ss, ms
    with open(filedialog.askopenfilename(), 'r') as f:
        pcl = eval(f.read())
    destroyVisuals()
    win.destroy()
    s = len(pcl)
    ss = s - 1
    ms = 0
    if s % 2 == 1: ms = int(round(ss / 2))
    cnvs.center = vector(ss / 2, ss / 2, ss / 2)
    for x in range(s):
        pl.append([])
        for y in range(s):
            pl[x].append([])
            for z in range(s):
                if (z == 0 or z == ss) or (y == 0 or y == ss) or (x == 0 or x == ss):
                    if ((y == 0 or y == ss) and (z == 0 or z == ss)) or (
                            (x == 0 or x == ss) and (y == 0 or y == ss)) or (
                            (x == 0 or x == ss) and (z == 0 or z == ss)):
                        pl[x][y].append(phantomObject(vector(x, y, z)))
                    else:
                        pl[x][y].append(box(canvas=cnvs, pos=vector(x, y, z), emmissive=True, shininess=0,
                                            color=vector(pcl[x][y][z][0], pcl[x][y][z][1], pcl[x][y][z][2])))
                        if z == 0:
                            pl[x][y][z].size = vector(1, 1, 0.001)
                            pl[x][y][z].pos.z = pl[x][y][z].pos.z + 0.4995
                        elif z == ss:
                            pl[x][y][z].size = vector(1, 1, 0.001)
                            pl[x][y][z].pos.z = pl[x][y][z].pos.z - 0.4995
                        elif y == 0:
                            pl[x][y][z].size = vector(1, 0.001, 1)
                            pl[x][y][z].pos.y = pl[x][y][z].pos.y + 0.4995
                        elif y == ss:
                            pl[x][y][z].size = vector(1, 0.001, 1)
                            pl[x][y][z].pos.y = pl[x][y][z].pos.y - 0.4995
                        elif x == 0:
                            pl[x][y][z].size = vector(0.001, 1, 1)
                            pl[x][y][z].pos.x = pl[x][y][z].pos.x + 0.4995
                        else:
                            pl[x][y][z].size = vector(0.001, 1, 1)
                            pl[x][y][z].pos.x = pl[x][y][z].pos.x - 0.4995
                else:
                    pl[x][y].append(phantomObject(vector(x, y, z)))
    connectInterface()


def doAlg():
    steps = str(alg.get()).split(' ')
    alg.set('')
    pcl = []
    for x in range(s):
        pcl.append([])
        for y in range(s):
            pcl[x].append([])
            for z in range(s):
                pcl[x][y].append((pl[x][y][z].color.x, pl[x][y][z].color.y, pl[x][y][z].color.z))
    try:
        for cmnd in steps:
            if len(cmnd) == 1:
                exec(cmndLib[cmnd])
            elif len(cmnd) == 2:
                if cmnd[1:2] in cmndLib.keys():
                    for n in range(eval(cmnd[0:1])):
                        exec(cmndLib[cmnd[1:2]])
                else:
                    exec(cmndLib[cmnd])
            elif len(cmnd) == 3:
                if cmnd[0:1] in cmndLib.keys():
                    exec(cmndLib[cmnd])
                else:
                    for n in range(eval(cmnd[0:1])):
                        exec(cmndLib[cmnd[1:3]])
            else:
                for n in range(eval(cmnd[0:1])):
                    exec(cmndLib[cmnd[1:4]])
    except:
        for x in range(s):
            for y in range(s):
                for z in range(s):
                    pl[x][y][z].color = vector(pcl[x][y][z][0], pcl[x][y][z][1], pcl[x][y][z][2])
        messagebox.showerror("Algorithm Entry Error",
                            "The algorithm entered is not correct!\nPlease check it,\nand try again.")


def shuffle():
    rs = ""
    try:
        for n in range(simpledialog.askinteger('Shuffle Input', 'Enter no. of times to shuffle:')):
            show_cmnd = choice(tuple(cmndLib.keys()))
            cmnd = cmndLib[show_cmnd]
            exec(cmnd)
            rs = rs + show_cmnd + ' '
        messagebox.showinfo('Shuffle List', rs)
        print(rs.split(' '))
    except:
        return


def solve():
    pass


def updateUndo(turn, n, t, r, ue):
    global redoList
    if ue:
        undoList.append((turn, n, t, r))
        redoList = []
    if redoList == []:
        redoBtn.configure(state='disabled')
    else:
        redoBtn.configure(state='enabled')
    if undoList == []:
        undoBtn.configure(state='disabled')
    else:
        undoBtn.configure(state='enabled')


def undo():
    cmnd = undoList.pop()
    redoList.append(cmnd)
    exec(f"{cmnd[0]}({cmnd[1]},{-1 * (cmnd[2])},{cmnd[3]},False)")


def redo():
    cmnd = redoList.pop()
    undoList.append(cmnd)
    exec(f"{cmnd[0]}({cmnd[1]},{cmnd[2]},{cmnd[3]},False)")


def addCEC(colour):
    global ceClr
    ceClr = colour
    ceccl.configure(text=f'Current Colour: {reverseColors[f"{ceClr}"]}')


def ceStart():
    ceccl.configure(text=f'Current Colour: {reverseColors[f"{pl[1][ss-1][ss].color}"]}')
    ce1b.configure(state='disabled')
    ce2b.configure(state='enabled')
    cenb.configure(state='enabled')
    cepb.configure(state='enabled')


def ceStop():
    global ceFace, ceClmn, ceRow, ceClr
    ceccl.configure(text='Current Colour: ')
    ce1b.configure(state='enabled')
    ce2b.configure(state='disabled')
    cenb.configure(state='disabled')
    cepb.configure(state='disabled')
    ceFace, ceClmn, ceRow, ceClr = 1, 1, 1, None
    cefl.configure(text='Face: Front')
    cecl.configure(text='Column: 1')
    cerl.configure(text='Row: 1')


def ceNext():
    global ceFace, ceClmn, ceRow, ceClr
    try:
        if ceClr is None:
            messagebox.showerror('Cube Entry Error', 'Please select a colour to continue.')
        elif ceFace == 1:
            pl[ceClmn][ss - ceRow][ss].color = ceClr
        elif ceFace == 2:
            pl[ceClmn][ss][ceRow].color = ceClr
        elif ceFace == 3:
            pl[ss][ss - ceRow][ss - ceClmn].color = ceClr
        elif ceFace == 4:
            pl[ceClmn][0][ss - ceRow].color = ceClr
        elif ceFace == 5:
            pl[0][ss - ceRow][ceClmn].color = ceClr
        elif ceFace == 6:
            pl[ss - ceClmn][ss - ceRow][0].color = ceClr
        ceRow += 1
        if ceRow > ss - 1:
            ceRow = 1
            ceClmn += 1
            if ceClmn > ss - 1:
                ceClmn = 1
                ceFace += 1
                if ceFace > 6:
                    ceFace = 1
        if ceFace == 1:
            ceClr = pl[ceClmn][ss - ceRow][ss].color
        elif ceFace == 2:
            ceClr = pl[ceClmn][ss][ceRow].color
        elif ceFace == 3:
            ceClr = pl[ss][ss - ceRow][ss - ceClmn].color
        elif ceFace == 4:
            ceClr = pl[ceClmn][0][ss - ceRow].color
        elif ceFace == 5:
            ceClr = pl[0][ss - ceRow][ceClmn].color
        elif ceFace == 6:
            ceClr = pl[ss - ceClmn][ss - ceRow][0].color

        cefl.configure(text=f'Face: {ceList[ceFace]}')
        cecl.configure(text=f'Column: {ceClmn}')
        cerl.configure(text=f'Row: {ceRow}')
        ceccl.configure(text=f'Current Colour: {reverseColors[f"{ceClr}"]}')
    except:
        pass


def cePrev():
    global ceFace, ceClmn, ceRow, ceClr
    try:
        if ceClr is None:
            messagebox.showerror('Cube Entry Error', 'Please select a colour to continue.')
        elif ceFace == 1:
            pl[ceClmn][ss - ceRow][ss].color = ceClr
        elif ceFace == 2:
            pl[ceClmn][ss][ceRow].color = ceClr
        elif ceFace == 3:
            pl[ss][ss - ceRow][ss - ceClmn].color = ceClr
        elif ceFace == 4:
            pl[ceClmn][0][ss - ceRow].color = ceClr
        elif ceFace == 5:
            pl[0][ss - ceRow][ceClmn].color = ceClr
        elif ceFace == 6:
            pl[ss - ceClmn][ss - ceRow][0].color = ceClr
        ceRow -= 1
        if ceRow < 1:
            ceRow = ss-1
            ceClmn -= 1
            if ceClmn < 1:
                ceClmn = ss-1
                ceFace -= 1
                if ceFace < 1:
                    ceFace = 6
        if ceFace == 1:
            ceClr = pl[ceClmn][ss - ceRow][ss].color
        elif ceFace == 2:
            ceClr = pl[ceClmn][ss][ceRow].color
        elif ceFace == 3:
            ceClr = pl[ss][ss - ceRow][ss - ceClmn].color
        elif ceFace == 4:
            ceClr = pl[ceClmn][0][ss - ceRow].color
        elif ceFace == 5:
            ceClr = pl[0][ss - ceRow][ceClmn].color
        elif ceFace == 6:
            ceClr = pl[ss - ceClmn][ss - ceRow][0].color

        cefl.configure(text=f'Face: {ceList[ceFace]}')
        cecl.configure(text=f'Column: {ceClmn}')
        cerl.configure(text=f'Row: {ceRow}')
        ceccl.configure(text=f'Current Colour: {reverseColors[f"{ceClr}"]}')
    except:
        pass


def adjustCEV(cevType,todo):
    if cevType=='Face':
        global ceFace
        if todo == '+':
            ceFace+=1
        elif todo == '-':
            ceFace-=1
        if ceFace>6: ceFace=1
        elif ceFace<1: ceFace=6
        cefl.configure(text=f'Face: {ceList[ceFace]}')
    elif cevType=='Clmn':
        global ceClmn
        if todo == '+':
            ceClmn+=1
        elif todo == '-':
            ceClmn-=1
        if ceClmn>ss-1: ceClmn=1
        elif ceClmn<1: ceClmn=ss-1
        cecl.configure(text=f'Column: {ceClmn}')
    elif cevType=='Row':
        global ceRow
        if todo == '+':
            ceRow+=1
        elif todo == '-':
            ceRow-=1
        if ceRow>ss-1: ceRow=1
        elif ceRow<1: ceRow=ss-1
        cerl.configure(text=f'Row: {ceRow}')


def connectVisuals():
    cnvs.userzoom = True
    cnvs.userspin = True
    cnvs.center = vector(ss / 2, ss / 2, ss / 2)

    for x in range(s):
        pl.append([])
        for y in range(s):
            pl[x].append([])
            for z in range(s):
                if (z == 0 or z == ss) or (y == 0 or y == ss) or (x == 0 or x == ss):
                    if ((y == 0 or y == ss) and (z == 0 or z == ss)) or (
                            (x == 0 or x == ss) and (y == 0 or y == ss)) or (
                            (x == 0 or x == ss) and (z == 0 or z == ss)):
                        pl[x][y].append(phantomObject(vector(x, y, z)))
                    else:
                        pl[x][y].append(box(canvas=cnvs, pos=vector(x, y, z), emmissive=True, shininess=0))
                        if z == 0:
                            pl[x][y][z].color = color.yellow
                            pl[x][y][z].size = vector(1, 1, 0.001)
                            pl[x][y][z].pos.z = pl[x][y][z].pos.z + 0.4995
                        elif z == ss:
                            pl[x][y][z].color = color.white
                            pl[x][y][z].size = vector(1, 1, 0.001)
                            pl[x][y][z].pos.z = pl[x][y][z].pos.z - 0.4995
                        elif y == 0:
                            pl[x][y][z].color = color.orange
                            pl[x][y][z].size = vector(1, 0.001, 1)
                            pl[x][y][z].pos.y = pl[x][y][z].pos.y + 0.4995
                        elif y == ss:
                            pl[x][y][z].color = color.red
                            pl[x][y][z].size = vector(1, 0.001, 1)
                            pl[x][y][z].pos.y = pl[x][y][z].pos.y - 0.4995
                        elif x == 0:
                            pl[x][y][z].color = color.blue
                            pl[x][y][z].size = vector(0.001, 1, 1)
                            pl[x][y][z].pos.x = pl[x][y][z].pos.x + 0.4995
                        else:
                            pl[x][y][z].color = color.green
                            pl[x][y][z].size = vector(0.001, 1, 1)
                            pl[x][y][z].pos.x = pl[x][y][z].pos.x - 0.4995
                else:
                    pl[x][y].append(phantomObject(vector(x, y, z)))


def connectInterface():
    global ms, ds, win, alg, solveBtn, undoBtn, redoBtn, cefl, cecl, cerl, ceccl, ce1b, ce2b, cepb, cenb

    def updateScrollCanvas(event):
        frmCnvs.configure(scrollregion=frmCnvs.bbox("all"))

    win = Tk()
    win.title('CubeInterfacer v2.8')
    win.geometry('+0+345') #win.geometry('+0+375')
    win.resizable(0, 0)
    menubar = Menu(win)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label='Open', command=openCube)
    filemenu.add_command(label='Save', command=saveCube)
    menubar.add_cascade(label='File', menu=filemenu)
    win.config(menu=menubar)

    controlPanel = ttk.Notebook(win)
    frm = ttk.Frame(controlPanel)
    frm.grid()
    controlPanel.add(frm, text='Remote')
    frm0 = ttk.Frame(frm)
    frm0.grid(column=0, row=0, rowspan=2)
    frm1 = ttk.LabelFrame(frm)
    frm1.grid(column=1, row=0)
    frm3 = ttk.LabelFrame(frm0, text='Cube Type')
    frm3.grid(pady=5, padx=4, columnspan=2)
    frm2 = ttk.LabelFrame(frm0, text='Algorithm Entry')
    frm2.grid(pady=5, padx=4, columnspan=2)
    frm4 = ttk.Frame(frm0)
    frm4.grid(row=2, pady=5, padx=4, columnspan=2, rowspan=3)

    ceFrame = ttk.Frame(controlPanel)
    ceFrame.grid()
    controlPanel.add(ceFrame, text='Cube Entry')
    ceCFrame = ttk.Frame(ceFrame)
    ceCFrame.grid(padx=100)

    camFrame = ttk.Frame(controlPanel)
    camFrame.grid()
    controlPanel.add(camFrame, text='Camera Controls')
    cubeTypeSelection = ttk.Spinbox(frm3, from_=2, to=100)
    cubeTypeSelection.set(s - 2)
    cubeTypeSelection.grid(column=1, row=1, padx=1)
    cubeTypeUpdater = ttk.Button(frm3, text='Update', command=lambda: updateCubeType(str(cubeTypeSelection.get())))
    cubeTypeUpdater.grid(column=2, row=1, padx=1)

    alg = StringVar()
    algEntry = ttk.Entry(frm2, textvariable=alg)
    algEntry.grid(column=0, row=0, padx=5)
    algBtn = ttk.Button(frm2, text='Do Steps', command=doAlg)
    algBtn.grid(column=1, row=0, padx=5)

    ttk.Button(frm4, text='Shuffle', command=shuffle).grid(column=0, row=0, pady=7)
    solveBtn = ttk.Button(frm4, text='Solve', command=solve)
    solveBtn.grid(column=1, row=0, pady=7)
    if s != 4: solveBtn.configure(state='disabled')
    undoBtn = ttk.Button(frm4, text='Undo', command=undo, state='disabled')
    undoBtn.grid(column=0, row=1, pady=7)
    redoBtn = ttk.Button(frm4, text='Redo', command=redo, state='disabled')
    redoBtn.grid(column=1, row=1, pady=7)
    ttk.Button(frm4, text='Reset', command=reset).grid(row=2, pady=7, columnspan=2)
    ttk.Button(frm4, text='Change Background Colour', command=changeCnvsClr).grid(row=3, padx=5, columnspan=2)

    frmCnvs = Canvas(frm1, width=350, height=260)#high due to my computer's increased text size - should be 300,225
    if ms != 0: frmCnvs.configure(height=345)#should be 300
    frmCnvs.pack()
    remote = ttk.Frame(frmCnvs)
    sbx = Scrollbar(frm1, orient="horizontal", command=frmCnvs.xview)
    sbx.pack(side="bottom", fill="x")
    # sby=Scrollbar(frm1,orient="vertical",command=frmCnvs.yview)
    # sby.pack(side="right",fill="y")
    frmCnvs.configure(xscrollcommand=sbx.set)  # ,yscrollcommand=sby.set)
    frmCnvs.create_window((0, 0), window=remote, anchor='nw')
    remote.bind("<Configure>", updateScrollCanvas)

    row = 0
    if ms == 0:
        cmndList = ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "X", "X'", "Y", "Y'", "Z", "Z'"]
    else:
        cmndList = ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'", "M", "M'", "E", "E'", "S", "S'",
                    "X", "X'", "Y", "Y'", "Z", "Z'"]
    for cmndNo in range(len(cmndList)):
        name = cmndList[cmndNo]
        clmn = cmndNo % 2
        exec(
            '''ttk.Button(remote,text=\""+name+"\",command=lambda:exec(cmndLib["''' + name + '''"])).grid(column=''' + str(
                clmn) + ''',row=''' + str(row) + ''')''')
        if name[1:2] == "'": row += 1

    if s > 5:
        row = 0
        cmndList = ["r", "r'", "l", "l'", "u", "u'", "d", "d'", "f", "f'", "b", "b'", "m", "m'", "e", "e'", "s", "s'"]
        for cmndNo in range(len(cmndList)):
            cmnd = str(cmndList[cmndNo])
            exec('''ttk.Button(remote,text="%s",command=lambda:exec(cmndLib["%s"])).grid(column=%i,row=%i)''' % (
                cmnd, cmnd, 2 + cmndNo % 2, row))
            if cmnd[1:2] == "'": row += 1

        ds = s - 2
        if s % 2 == 1: ds = s - 3
        ds = int((ds / 2) - 1)
        cmndList = ['R', 'L', 'U', 'D', 'F', 'B']
        for tt in range(2, ds + 2):
            for cmndNo in range(6):
                name = cmndList[cmndNo]
                show_name = name + str(tt)  # name+'\\'+'u208'+str(tt)
                exec("ttk.Button(remote,text='%s',command=lambda:%sn(%i,1,%i)).grid(column=%i,row=%i)" % (
                    show_name, name, tt, tt + 1, 2 * tt, cmndNo))
                exec('''ttk.Button(remote,text="%s'",command=lambda:%sn(%i,-1,%i)).grid(column=%i,row=%i)''' % (
                    show_name, name, tt, tt + 1, 2 * tt + 1, cmndNo))
                exec('''cmndLib["%s%i"] = "%sn(%i,1,%i)"''' % (name, tt, name, tt, tt + 1))
                exec('''cmndLib["%s%i'"] = "%sn(%i,-1,%i)"''' % (name, tt, name, tt, tt + 1))
    del cmndList

    ce1b = ttk.Button(ceCFrame, text='Start',command=ceStart)
    ce1b.grid(pady=5)
    ce2b = ttk.Button(ceCFrame, text='Stop', state='disabled',command=ceStop)
    ce2b.grid(column=8, row=0)

    ceBFrame = ttk.Frame(ceCFrame)
    ceBFrame.grid(column=0, row=1, padx=10, pady=10, columnspan=9, rowspan=2)
    ceDFrame = ttk.Frame(ceCFrame)
    ceDFrame.grid(column=0, row=3, pady=5, columnspan=9, rowspan=2)
    ceccf=ttk.Frame(ceDFrame)
    ceccf.grid(column=2, row=1, pady=20, columnspan=5)

    Button(ceBFrame, background='white', width=10, height=2, command=lambda: addCEC(color.white)).grid()
    Button(ceBFrame, background='orange', width=10, height=2, command=lambda: addCEC(color.orange)).grid(column=1,
                                                                                                        row=0)
    Button(ceBFrame, background='green', width=10, height=2, command=lambda: addCEC(color.green)).grid(column=2, row=0)
    Button(ceBFrame, background='red', width=10, height=2, command=lambda: addCEC(color.red)).grid(row=1)
    Button(ceBFrame, background='blue', width=10, height=2, command=lambda: addCEC(color.blue)).grid(column=1, row=1)
    Button(ceBFrame, background='yellow', width=10, height=2, command=lambda: addCEC(color.yellow)).grid(column=2,
                                                                                                        row=1)

    ttk.Button(ceDFrame,text='+',command=lambda:adjustCEV('Face','+'),width=1).grid(column=0, row=0)
    ttk.Button(ceDFrame,text='+',command=lambda:adjustCEV('Clmn','+'),width=1).grid(column=3, row=0)
    ttk.Button(ceDFrame,text='+',command=lambda:adjustCEV('Row','+'),width=1).grid(column=6, row=0)
    cefl = ttk.Label(ceDFrame, text='Face: Front')
    cefl.grid(column=1, row=0, padx=5)
    cecl = ttk.Label(ceDFrame, text='Column: 1')
    cecl.grid(column=4, row=0, padx=5)
    cerl = ttk.Label(ceDFrame, text='Row: 1')
    cerl.grid(column=7, row=0, padx=5)
    ttk.Button(ceDFrame,text='-',command=lambda:adjustCEV('Face','-'),width=1).grid(column=2, row=0)
    ttk.Button(ceDFrame,text='-',command=lambda:adjustCEV('Clmn','-'),width=1).grid(column=5, row=0)
    ttk.Button(ceDFrame,text='-',command=lambda:adjustCEV('Row','-'),width=1).grid(column=8, row=0)
    ceccl = ttk.Label(ceccf, text='Current Colour: ')
    ceccl.grid(padx=10,columnspan=5)
    cepb = ttk.Button(ceDFrame, text='Previous', command=cePrev,state='disabled')
    cepb.grid(column=0, row=1, columnspan=2)
    cenb = ttk.Button(ceDFrame, text='Next', command=ceNext,state='disabled')
    cenb.grid(column=7, row=1, columnspan=2)

    controlPanel.grid()
    win.mainloop()


def vCube(cubeType=3):
    global s, ss, ms, cmndLib
    s = int(cubeType + 2)
    ss = s - 1
    ms = 0
    cmndLib = {
        "R": "Rn(0,1,2)", "R'": "Rn(0,-1,2)", "L": "Ln(0,1,2)", "L'": "Ln(0,-1,2)",
        "U": "Un(0,1,2)", "U'": "Un(0,-1,2)", "D": "Dn(0,1,2)", "D'": "Dn(0,-1,2)",
        "F": "Fn(0,1,2)", "F'": "Fn(0,-1,2)", "B": "Bn(0,1,2)", "B'": "Bn(0,-1,2)",
        "X": "Ln(0,-1,s)", "X'": "Ln(0,1,s)", "Y": "Dn(0,-1,s)", "Y'": "Dn(0,1,s)", "Z": "Bn(0,-1,s)",
        "Z'": "Bn(0,1,s)",
        "r": "Rn(0,1,ds+2)", "r'": "Rn(0,-1,ds+2)", "l": "Ln(0,1,ds+2)", "l'": "Ln(0,-1,ds+2)",
        "u": "Un(0,1,ds+2)", "u'": "Un(0,-1,ds+2)", "d": "Dn(0,1,ds+2)", "d'": "Dn(0,-1,ds+2)",
        "f": "Fn(0,1,ds+2)", "f'": "Fn(0,-1,ds+2)", "b": "Bn(0,1,ds+2)", "b'": "Bn(0,-1,ds+2)"}
    if s % 2 == 1:
        ms = int(round(ss / 2))
        cmndLib["M"], cmndLib["M'"], cmndLib["E"], cmndLib["E'"], cmndLib["S"], cmndLib[
            "S'"] = "Ln(ms,1,ms+1)", "Ln(ms,-1,ms+1)", "Dn(ms,1,ms+1)", "Dn(ms,-1,ms+1)", "Bn(ms,1,ms+1)", "Bn(ms,-1,ms+1)"
    if s > 5:
        cmndLib["m"], cmndLib["m'"], cmndLib["e"], cmndLib["e'"], cmndLib["s"], cmndLib[
            "s'"] = "Ln(2,1,ss-1)", "Ln(2,-1,ss-1)", "Dn(2,1,ss-1)", "Dn(2,-1,ss-1)", "Bn(2,1,ss-1)", "Bn(2,-1,ss-1)"
    connectVisuals()
    connectInterface()


#vCube(3)
