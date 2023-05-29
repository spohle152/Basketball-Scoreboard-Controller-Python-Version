#Functions for interface items

#Get links between input and output through entries on the mode 1 interface
#Read and update variables based off input
#Compare Scores, Fouls, and Timeouts to separate quarters and make new signals work
#Write the variables to a file

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time as t
from threading import Thread
import json

period=1
periodString = "1st"
hscore=[0,0,0,0]
vscore=[0,0,0,0]
hbonus=0
vbonus=0
hdbonus=0
vdbonus=0
hfouls=0
vfouls=0
htol=5
vtol=5
hposs=0
vposs=0
timeOn=0
min=8
sec=0
tenth=0
newhfoul = 0
newvfoul = 0
newhtimeout = 0
newvtimeout = 0
clock="8:00"
output_file= ""
input_file = ""
freezeVar=0
x=0
class new(Thread):
    def run(self):
        global newhfoul
        global newvfoul
        global newhtimeout
        global newvtimeout
        t.sleep(8)
        newhfoul=0
        newvfoul=0
        newhtimeout=0
        newvtimeout=0
        writeFile(output_file)


class read_file(Thread):
    def run(self):
        global period
        global hposs
        global vposs
        global hscore
        global htol
        global vtol
        global newhfoul
        global newvfoul
        global newhtimeout
        global newvtimeout
        global hfouls
        global vfouls
        global hbonus
        global hdbonus
        global vbonus
        global vdbonus
        global clock
        global x
        while (True):
            f = open(input_file)
            data=json.load(f)[0]
            try:
                if (period != int(data[periodFile.get()])): 
                    period = int(data[periodFile.get()])
                    update_period()
            except: x=1
            try: hposs = int(data[hpossFile.get()])
            except: x=1
            try: vposs = int(data[vpossFile.get()])
            except: x=1
            try: 
                if (sum(hscore) != int(data[hscoreFile.get()])): hscore[period-1] += (int(data[hscoreFile.get()])-sum(hscore))
            except: x=1
            try:
                if (sum(vscore) != int(data[vscoreFile.get()])): vscore[period-1] += (int(data[vscoreFile.get()])-sum(vscore))
            except: x=1
            try:
                if (htol != int(data[htolFile.get()])):
                    htol=int(data[htolFile.get()])
                    newhtimeout = 1
                    newrunnable = new()
                    newrunnable.start()
            except: x=1
            try:
                if (vtol != int(data[vtolFile.get()])):
                    vtol=int(data[vtolFile.get()])
                    newvtimeout = 1
                    newrunnable = new()
                    newrunnable.start()
            except:x=1
            try:
                if (hfouls != int(data[hfoulFile.get()])):
                    hfouls=int(data[hfoulFile.get()])
                    newhfoul = 1
                    newrunnable = new()
                    newrunnable.start()
                    if hfouls >= 7:
                        vbonus = 1
                    else:
                        vbonus = 0
                    if vfouls >= 10:
                        vdbonus = 1
                    else:
                        vdbonus = 0
            except: x=1
            try:
                if (vfouls != int(data[vfoulFile.get()])):
                    vfouls=int(data[vfoulFile.get()])
                    newvfoul = 1
                    newrunnable = new()
                    newrunnable.start()
                    if vfouls >= 7:
                        hbonus = 1
                    else:
                        hbonus = 0
                    if vfouls >= 10:
                        hdbonus = 1
                    else:
                        hdbonus = 0
            except: x=1
            try: clock = data[clockFile.get()]
            except: x=1
            writeFile(output_file)


        



class clock_runner(Thread):
    def run(self):
        global timeOn
        global min
        global sec
        global tenth
        time = t.time()*1000; #the amount of time since the last update

        while (timeOn):
            if (t.time()*1000 >= time):
                time+=100
                if (timeOn and (min != 0 or sec != 0 or tenth != 0)): #Add logic to have timer count down correctly
                    if (sec == 0 and min != 0 and tenth == 0):
                        min-=1
                        sec = 59
                        tenth = 10
                    if (tenth == 0 and sec != 0):
                        sec-=1
                        tenth = 10
                    tenth-=1
            try:
                writeFile(output_file) #Send the new clock data to the file to be outputted
            except:
                print("Opps! Something Interrupted me!")
            t.sleep(0.05)

def reset():
    global period
    global periodString
    global hscore
    global vscore
    global hbonus
    global vbonus
    global hdbonus
    global vdbonus
    global hfouls
    global vfouls
    global htol
    global vtol
    global hposs
    global vposs
    global timeOn
    global min
    global sec
    global tenth
    global clock
    period=1
    periodString = "1st"
    hscore=[0,0,0,0]
    vscore=[0,0,0,0]
    hbonus=0
    vbonus=0
    hdbonus=0
    vdbonus=0
    hfouls=0
    vfouls=0
    htol=5
    vtol=5
    if (hposs == 1): toggleHomePoss()
    if (vposs == 1): toggleVisitorPoss()
    timeOn=1
    min=8
    sec=0
    tenth=0
    clock="8:00"
    writeFile(output_file)

def foulReset():
    global hbonus
    global hdbonus
    global vbonus
    global vdbonus
    global hfouls
    global vfouls
    hbonus=0
    hdbonus=0
    vbonus=0
    vdbonus=0
    hfouls=0
    vfouls=0
    writeFile(output_file)

top = tk.Tk()
# icon = tk.PhotoImage(file = 'JCD LIVE LOGO 1 .png')
# top.wm_iconphoto(False, icon)
top.title("Scoreboard Controller")
top.geometry("1200x550")
var = tk.IntVar()

homeName=StringVar()
homeName.set("Home")
visitorName=StringVar()
visitorName.set("Visitor")
hscoreVar = StringVar()
vscoreVar = StringVar()
hpointsPerQuarterLabel = StringVar()
vpointsPerQuarterLabel = StringVar()
selected_footer = IntVar()
selected_header = IntVar()

def writeFile (outputFile):
    global x
    global clock
    if (freezeVar == 0):
        hscoreVar.set(homeName.get() + " Score: "+str(sum(hscore)))
        vscoreVar.set(visitorName.get() + " Score: "+str(sum(vscore)))
        periodStringVar.set("Period: "+periodString)
        hTOLLabel.set(homeName.get()+" TOL: "+str(htol))
        vTOLLabel.set(visitorName.get()+" TOL: "+str(vtol))
        hFoulLabel.set(homeName.get()+" Fouls: "+str(hfouls))
        vFoulLabel.set(visitorName.get()+" Fouls: "+str(vfouls))
        try:
            h3Text.set(homeName.get()+" +3")
            h2Text.set(homeName.get()+" +2")
            h1Text.set(homeName.get()+" +1")
            hmText.set(homeName.get()+" -1")
            v3Text.set(visitorName.get()+" +3")
            v2Text.set(visitorName.get()+" +2")
            v1Text.set(visitorName.get()+" +1")
            vmText.set(visitorName.get()+" -1")
        except: x=1
        hpointsPerQuarterLabel.set(homeName.get()+" Points Per Quarter: 1st-" + str(hscore[0]) + " | 2nd-" + str(hscore[1]) + " | 3rd-" + str(hscore[2]) + " | 4th-" + str(hscore[3]))
        vpointsPerQuarterLabel.set(visitorName.get()+" Points Per Quarter: 1st-" + str(vscore[0]) + " | 2nd-" + str(vscore[1]) + " | 3rd-" + str(vscore[2]) + " | 4th-" + str(vscore[3]))
        if (clicked.get()=="Full Controller"):
            if min==0:
                clock = str(sec)+"."+str(tenth)
            else:
                clock = str(min)+":"+"{x:02d}".format(x=sec)
        clockVar.set("Clock: "+clock)
        header = ""
        footer = ""
        if selected_header.get() == 1: header = hpointsPerQuarterLabel.get()
        elif selected_header.get() == 2: header = vpointsPerQuarterLabel.get()
        elif selected_header.get() == 3: header = customHeadervalue.get()
        else: header = ""
        if selected_footer.get() == 1: footer = hpointsPerQuarterLabel.get()
        elif selected_footer.get() == 2: footer = vpointsPerQuarterLabel.get()
        elif selected_footer.get() == 3: footer = customFootervalue.get()
        else: footer = ""
        headerActive = 0
        footerActive = 0
        if (selected_header.get()==4): headerActive=0
        else: headerActive=1
        if (selected_footer.get()==4): footerActive=0
        else: footerActive=1
        f = open(outputFile+"/scoreboard.json", "w")
        f.write("[{\"Clock\":\""+clock+ "\", \"Period\":\""+periodString+"\", \"HeaderActive\":\""+str(headerActive)+"\", \"HeaderText\":\""+header+"\", \"FooterActive\":\""+str(footerActive)+"\", \"FooterText\":\""+footer+"\",\"HomeName\":\""+homeName.get()+"\", \"HomeScore\":\""+str(sum(hscore))+ "\", \"VisitorName\":\""+visitorName.get()+"\",\"VisitorScore\":\""+str(sum(vscore))+"\", \"HomePoss\":\""+str(hposs)+"\", \"VisitorPoss\":\""+str(vposs)+"\", \"HomeBonus\":\""+str(hbonus)+"\", \"HomeDoubleBonus\":\""+str(hdbonus)+"\", \"VisitorBonus\":\""+str(vbonus)+"\", \"VisitorDoubleBonus\":\""+str(vdbonus)+"\", \"HomeFouls\":\""+str(hfouls)+"\",  \"NewHomeFoul\":\""+str(newhfoul)+"\", \"VisitorFouls\":\""+str(vfouls)+"\",  \"NewVisitorFoul\":\""+str(newvfoul)+"\",\"HomeTOL\":\""+str(htol)+"\",  \"NewHomeTimeout\":\""+str(newhtimeout)+"\",\"VisitorTOL\":\""+str(vtol)+"\", \"NewVisitorTimeout\":\""+str(newvtimeout)+"\"}]")
def clearFrame():
    # destroy all widgets from frame
    for widget in top.winfo_children():
        widget.destroy()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()

def exit(e):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        top.destroy()
def save_output_file():
    filepath = filedialog.askdirectory()
    global output_file
    output_file = filepath

def get_input_file():
    files = [("JSON Files", ".json")]
    filepath = filedialog.askopenfilename(title="Select Input File", filetypes=files)
    global input_file
    input_file = filepath
    
def update_period():
    global periodString
    if period == 1: periodString = "1st"
    elif period == 2: periodString = "2nd"
    elif period == 3: periodString = "3rd"
    elif period <= 20: periodString = str(period)+"th"
    else: periodString = str(period)
    writeFile (output_file)

def update_ot():
    global periodString
    periodString="OT"
    writeFile (output_file)

def change_focus(event):
    event.widget.focus_set()
top.bind_all('<Button>', change_focus)
#Check File Function
#Get Mode and Output File
mode_label = Label(top, text="Enter the Mode of Functionality for the controller")
mode_label.grid()
mode_options= ["Pass-through with input file", "Full Controller"]
clicked = StringVar()
clicked.set("Pass-through with input file")
mode_selected = OptionMenu(top, clicked, *mode_options)
mode_selected.grid()
browse_output_file = Button(top, text="Select Output Folder", command=save_output_file)
browse_output_file.grid()
submit = Button (top, text="Submit", command=lambda: var.set(1))
submit.grid()
submit.wait_variable(var)
while (output_file == ""):
    tk.messagebox.showerror(title="ERROR", message="Please Select An Output Folder")
    submit.wait_variable(var)
clearFrame()
#Mode 1 Setup (Pass through)
if (clicked.get()=="Pass-through with input file"):
    file_label = Label(top, text="Get the input file to extract scoreboard data from")
    file_label.grid()
    browse_input_file = Button(top, text="Select Input .json File", command=get_input_file)
    browse_input_file.grid()
    submit = Button (top, text="Submit", command=lambda: var.set(1))
    submit.grid()
    submit.wait_variable(var)
    while (input_file == ""):
        tk.messagebox.showerror(title="ERROR", message="Please Select An Output Folder")
        submit.wait_variable(var)
    clearFrame()
    #Start Reading File
    inputrunnable = read_file()
    inputrunnable.start()
    #Mode 1 Interface
    clockVar=StringVar()
    clockVar.set("Clock: "+clock)
    clockLabel = Label (top, textvariable=clockVar).place(x=30, y=400)
    clockFile=StringVar()
    clockFile.set("Clock")
    clockFileEnter = Entry(top, textvariable=clockFile).place(x=130,y=400,width=250,height=20)
    periodStringVar=StringVar()
    periodStringVar.set("Period: "+periodString)
    periodFile = StringVar()
    periodFile.set("Period(Number)")
    periodFileEnter = Entry(top, textvariable=periodFile).place(x=110,y=10,width=240,height=20)
    periodLabel = Label (top, textvariable=periodStringVar).place(x=10,y=10, width=100, height=20)
    def period_ot():
        update_ot()
    periodOT = Button (top, text= "OT", command=period_ot).place(x=300, y=10, width=50, height=20)
    home = Entry(top, textvariable=homeName)
    home.place(x=30, y=50, width=100, height=20)
    hpossFile=StringVar()
    hpossFile.set("HPoss")
    hpossFileEnter = Entry(top, textvariable=hpossFile).place(x=30,y=80,width=150,height=20)
    homeName.trace('w', lambda name, index, mode, sv=homeName: writeFile(output_file))
    hscoreVar.set(homeName.get() + " Score: "+str(sum(hscore)))
    hscoreLabel = Label (top, textvariable=hscoreVar).place(x=30, y=110, width=150, height=20)
    hscoreFile = StringVar()
    hscoreFile.set("hScore")
    hscoreFileEnter = Entry(top, textvariable=hscoreFile).place(x=30,y=140,width=150,height=20)
    visitor = Entry(top, textvariable=visitorName).place(x=370, y=50, width=100, height=20)
    visitorName.trace('w', lambda name, index, mode, sv=visitorName: writeFile(output_file))
    vpossFile=StringVar()
    vpossFile.set("VPoss")
    vpossFileEnter = Entry(top, textvariable=vpossFile).place(x=370,y=80,width=150,height=20)
    vscoreVar.set(visitorName.get() + " Score: "+str(sum(vscore)))
    vscoreLabel = Label (top, textvariable=vscoreVar).place(x=370, y=110, width=150, height=20)
    vscoreFile = StringVar()
    vscoreFile.set("vScore")
    vscoreFileEnter = Entry(top, textvariable=vscoreFile).place(x=370,y=140,width=150,height=20)
    homeTOL = Label (top, text="TOL: 5")
    visitorTOL = Label (top, text="TOL: 5")
    hFoulsLabel = Label (top, text="Fouls: 0")
    vFoulsLabel = Label (top, text="Fouls: 0")
    def toggleFreeze():
        global freezeVar
        if freeze.config('relief')[-1] == 'sunken':
            freeze.config(relief="raised")
            freezeVar=0
        else:
            freeze.config(relief="sunken")
            freezeVar=1
    freeze = Button (top, text="Freeze", relief="raised", command=toggleFreeze)
    freeze.place(x=250, y=100, width=100, height=20)
    hTOLLabel=StringVar()
    hTOLLabel.set(homeName.get()+" TOL: "+str(htol))
    hTOL = Label(top, textvariable=hTOLLabel).place(x=30, y=260, width=150, height=20)
    htolFile = StringVar()
    htolFile.set("hTOL")
    htolFileEnter = Entry(top, textvariable=htolFile).place(x=30,y=290,width=100,height=20)

    vTOLLabel=StringVar()
    vTOLLabel.set(visitorName.get()+" TOL: "+str(vtol))
    vTOL = Label(top, textvariable=vTOLLabel).place(x=370, y=260, width=150, height=20)
    vtolFile = StringVar()
    vtolFile.set("vTOL")
    vtolFileEnter = Entry(top, textvariable=vtolFile).place(x=370,y=290,width=100,height=20)

    hFoulLabel=StringVar()
    hFoulLabel.set(homeName.get()+" Fouls: "+str(hfouls))
    hFouls = Label(top, textvariable=hFoulLabel).place(x=30, y=320, width=150, height=20)
    hfoulFile = StringVar()
    hfoulFile.set("hFouls")
    hfoulFileEnter = Entry(top, textvariable=hfoulFile).place(x=30,y=350,width=100,height=20)
    vFoulLabel=StringVar()
    vFoulLabel.set(visitorName.get()+" Fouls: "+str(vfouls))
    vFouls = Label(top, textvariable=vFoulLabel).place(x=370, y=320, width=150, height=20)
    vfoulFile = StringVar()
    vfoulFile.set("vFouls")
    vfoulFileEnter = Entry(top, textvariable=vfoulFile).place(x=370,y=350,width=100,height=20)
    HeaderLabel = Label(top, text="Header").place(x=600, y=10, width=450, height=20)
    customHeaderLabel = Label(top, text="Enter a Custom Header Here:").place(x=600, y=40,width=450,height=20)
    customHeadervalue = StringVar()
    customHeadervalue.set("Enter a Custom Header")
    customHeader = Entry(top, textvariable=customHeadervalue)
    customHeader.place(x=600, y=70,width=450,height=20)
    customHeadervalue.trace('w', lambda name, index, mode, sv=customHeadervalue: writeFile(output_file))
    hpointsPerQuarterLabel.set(homeName.get()+" Points Per Quarter: 1st-" + str(hscore[0]) + " | 2nd-" + str(hscore[1]) + " | 3rd-" + str(hscore[2]) + " | 4th-" + str(hscore[3]))
    hpointsPerQuarter = Radiobutton(top, textvariable=hpointsPerQuarterLabel, value = 1, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=100,width=450,height=20)
    vpointsPerQuarterLabel.set(visitorName.get()+" Points Per Quarter: 1st-" + str(vscore[0]) + " | 2nd-" + str(vscore[1]) + " | 3rd-" + str(vscore[2]) + " | 4th-" + str(vscore[3]))
    vpointsPerQuarter = Radiobutton(top, textvariable=vpointsPerQuarterLabel, value = 2, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=130,width=450,height=20)
    customHeader = Radiobutton(top, textvariable=customHeadervalue, value=3, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=160,width=450,height=20)
    blankHeader = Radiobutton(top, text="Blank", value=4, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=190,width=450,height=20)

    FooterLabel = Label(top, text="Footer").place(x=600, y=250, width=450, height=20)
    customFooterLabel = Label(top, text="Enter a Custom Footer Here:").place(x=600, y=280,width=450,height=20)
    customFootervalue = StringVar()
    customFootervalue.set("Enter a Custom Footer")
    customFooter = Entry(top, textvariable=customFootervalue)
    customFooter.place(x=600, y=310,width=450,height=20)
    customFootervalue.trace('w', lambda name, index, mode, sv=customFootervalue: writeFile(output_file))
    hfpointsPerQuarter = Radiobutton(top, textvariable=hpointsPerQuarterLabel, value = 1, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=340,width=450,height=20)
    vfpointsPerQuarter = Radiobutton(top, textvariable=vpointsPerQuarterLabel, value = 2, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=370,width=450,height=20)
    customFooter = Radiobutton(top, textvariable=customFootervalue, value=3, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=400,width=450,height=20)
    blankFooter = Radiobutton(top, text="Blank", value=4, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=430,width=450,height=20)
    selected_footer.set(4)
    selected_header.set(4)
#Mode 2 Interface
if (clicked.get()=="Full Controller"):
    clockVar=StringVar()
    clockVar.set("Clock: "+clock)
    clockLabel = Label (top, textvariable=clockVar).place(x=30, y=400)
    periodStringVar=StringVar()
    periodStringVar.set("Period: "+periodString)
    periodLabel = Label (top, textvariable=periodStringVar).place(x=10,y=10, width=100, height=20)
    def period_minus():
        global period
        period = period-1
        update_period()
    periodMinus = Button (top, text= "-", command=period_minus).place(x=100, y=10, width=50, height=20)
    def period_plus():
        global period
        global min
        global sec
        global tenth
        period = period+1
        if (hposs == 1 and vposs==0):
            toggleVisitorPoss()
        elif (hposs == 0 and vposs==1):
            toggleHomePoss()
        min=8
        sec=0
        tenth=0
        if (period > 4):
            hscore.append(0)
            vscore.append(0)
        update_period()
    periodPlus = Button (top, text= "+", command=period_plus).place(x=150, y=10, width=50, height=20)
    def period_ot():
        update_ot()
    periodOT = Button (top, text= "OT", command=period_ot).place(x=200, y=10, width=50, height=20)
    home = Entry(top, textvariable=homeName).place(x=30, y=50, width=100, height=20)
    homeName.trace('w', lambda name, index, mode, sv=homeName: writeFile(output_file))
    hscoreVar = StringVar()
    hscoreVar.set(homeName.get() + " Score: "+str(sum(hscore)))
    hscoreLabel = Label (top, textvariable=hscoreVar).place(x=30, y=110, width=150, height=20)
    visitor = Entry(top, textvariable=visitorName)
    visitor.place(x=370, y=50, width=100, height=20)
    visitorName.trace('w', lambda name, index, mode, sv=visitorName: writeFile(output_file))
    vscoreVar = StringVar()
    vscoreVar.set(visitorName.get() + " Score: "+str(sum(vscore)))
    vscoreLabel = Label (top, textvariable=vscoreVar).place(x=370, y=110, width=150, height=20)
    def toggleHomePoss():
        global hposs
        if homePoss.config('relief')[-1] == 'sunken':
            homePoss.config(relief="raised")
            hposs=0
        else:
            homePoss.config(relief="sunken")
            hposs=1
            if (vposs == 1):
                toggleVisitorPoss()
        writeFile(output_file)
    homePoss = Button (top, text="<", relief="raised", command=toggleHomePoss)
    homePoss.place(x=30, y=80, width=50, height=20)
    def toggleVisitorPoss():
        global vposs
        if visitorPoss.config('relief')[-1] == 'sunken':
            visitorPoss.config(relief="raised")
            vposs=0
        else:
            visitorPoss.config(relief="sunken")
            vposs=1
            if (hposs == 1):
                toggleHomePoss()
        writeFile(output_file)
    visitorPoss = Button (top, text=">", relief="raised", command=toggleVisitorPoss)
    visitorPoss.place(x=370, y=80, width=50, height=20)
    homeTOL = Label (top, text="TOL: 5")
    visitorTOL = Label (top, text="TOL: 5")
    hFoulsLabel = Label (top, text="Fouls: 0")
    vFoulsLabel = Label (top, text="Fouls: 0")
    def toggleFreeze():
        global freezeVar
        if freeze.config('relief')[-1] == 'sunken':
            freeze.config(relief="raised")
            freezeVar=0
        else:
            freeze.config(relief="sunken")
            freezeVar=1
    freeze = Button (top, text="Freeze", relief="raised", command=toggleFreeze)
    freeze.place(x=250, y=100, width=100, height=20)
    h3Text = StringVar()
    h3Text.set(homeName.get()+" +3")
    def homeplus3():
        hscore[period-1]+=3
        writeFile(output_file)
    h3 = Button(top, textvariable=h3Text, command=homeplus3).place(x=30, y=140, width=150, height=20)
    h2Text = StringVar()
    h2Text.set(homeName.get()+" +2")
    def homeplus2():
        hscore[period-1]+=2
        writeFile(output_file)
    h2 = Button(top, textvariable=h2Text, command=homeplus2).place(x=30, y=170, width=150, height=20)
    h1Text = StringVar()
    h1Text.set(homeName.get()+" +1")
    def homeplus1():
        hscore[period-1]+=1
        writeFile(output_file)
    h1 = Button(top, textvariable=h1Text, command=homeplus1).place(x=30, y=200, width=150, height=20)
    hmText = StringVar()
    hmText.set(homeName.get()+" -1")
    def homeminus1():
        hscore[period-1]-=1
        writeFile(output_file)
    hm = Button(top, textvariable=hmText, command=homeminus1).place(x=30, y=230, width=150, height=20)

    v3Text = StringVar()
    v3Text.set(visitorName.get()+" +3")
    def visitorplus3():
        vscore[period-1]+=3
        writeFile(output_file)
    v3 = Button(top, textvariable=v3Text, command=visitorplus3).place(x=370, y=140, width=150, height=20)
    v2Text = StringVar()
    v2Text.set(visitorName.get()+" +2")
    def visitorplus2():
        vscore[period-1]+=2
        writeFile(output_file)
    v2 = Button(top, textvariable=v2Text, command=visitorplus2).place(x=370, y=170, width=150, height=20)
    v1Text = StringVar()
    v1Text.set(visitorName.get()+" +1")
    def visitorplus1():
        vscore[period-1]+=1
        writeFile(output_file)
    v1 = Button(top, textvariable=v1Text, command=visitorplus1).place(x=370, y=200, width=150, height=20)
    vmText = StringVar()
    vmText.set(visitorName.get()+" -1")
    def visitorminus1():
        vscore[period-1]-=1
        writeFile(output_file)
    vm = Button(top, textvariable=vmText, command=visitorminus1).place(x=370, y=230, width=150, height=20)

    hTOLLabel=StringVar()
    hTOLLabel.set(homeName.get()+" TOL: "+str(htol))
    hTOL = Label(top, textvariable=hTOLLabel).place(x=30, y=260, width=150, height=20)
    def htolplus1():
        global htol
        htol+=1
        writeFile(output_file)
    htolPlus = Button(top, text="+", command=htolplus1).place(x=80, y=290, width=50, height=20)
    def htolminus1():
        global htol
        global newhtimeout
        htol-=1
        newhtimeout=1
        newrunnable = new()
        newrunnable.start()
        writeFile(output_file)
    htolMinus = Button(top, text="-", command=htolminus1).place(x=30, y=290, width=50, height=20)

    vTOLLabel=StringVar()
    vTOLLabel.set(visitorName.get()+" TOL: "+str(vtol))
    vTOL = Label(top, textvariable=vTOLLabel).place(x=370, y=260, width=150, height=20)
    def vtolplus1():
        global vtol
        vtol+=1
        writeFile(output_file)
    vtolPlus = Button(top, text="+", command=vtolplus1).place(x=420, y=290, width=50, height=20)
    def vtolminus1():
        global vtol
        global newvtimeout
        vtol-=1
        newvtimeout=1
        newrunnable = new()
        newrunnable.start()
        writeFile(output_file)
    vtolMinus = Button(top, text="-", command=vtolminus1).place(x=370, y=290, width=50, height=20)

    hFoulLabel=StringVar()
    hFoulLabel.set(homeName.get()+" Fouls: "+str(hfouls))
    hFouls = Label(top, textvariable=hFoulLabel).place(x=30, y=320, width=150, height=20)
    def hfoulplus1():
        global hfouls
        global newhfoul
        global vbonus
        global vdbonus
        hfouls+=1
        newhfoul=1
        newrunnable = new()
        newrunnable.start()
        if hfouls >= 7:
            vbonus = 1
        else:
            vbonus = 0
        if hfouls >= 10:
            vdbonus = 1
        else:
            vdbonus = 0
        writeFile(output_file)
    hFoulPlus = Button(top, text="+", command=hfoulplus1).place(x=80, y=350, width=50, height=20)
    def hfoulminus1():
        global hfouls
        global vbonus
        global vdbonus
        hfouls-=1
        if hfouls >= 7:
            vbonus = 1
        else:
            vbonus = 0
        if hfouls >= 10:
            vdbonus = 1
        else:
            vdbonus = 0
        writeFile(output_file)
    hFoulMinus = Button(top, text="-", command=hfoulminus1).place(x=30, y=350, width=50, height=20)

    vFoulLabel=StringVar()
    vFoulLabel.set(visitorName.get()+" Fouls: "+str(vfouls))
    vFouls = Label(top, textvariable=vFoulLabel).place(x=370, y=320, width=150, height=20)
    def vfoulplus1():
        global vfouls
        global newvfoul
        global hbonus
        global hdbonus
        vfouls+=1
        newvfoul=1
        newrunnable = new()
        newrunnable.start()
        if vfouls >= 7:
            hbonus = 1
        else:
            hbonus = 0
        if vfouls >= 10:
            hdbonus = 1
        else:
            hdbonus = 0
        writeFile(output_file)
    vfoulPlus = Button(top, text="+", command=vfoulplus1).place(x=420, y=350, width=50, height=20)
    def vfoulminus1():
        global vfouls
        global hbonus
        global hdbonus
        vfouls-=1
        if vfouls >= 7:
            hbonus = 1
        else:
            hbonus = 0
        if vfouls >= 10:
            hdbonus = 1
        else:
            hdbonus = 0
        writeFile(output_file)
    vfoulMinus = Button(top, text="-", command=vfoulminus1).place(x=370, y=350, width=50, height=20)

    reset_button = Button(top, text="Reset", command=reset).place(x=250, y=40, width=100, height=20)
    foul_reset_button = Button(top, text="Foul Reset", command=foulReset).place(x=250, y=70, width=100, height=20)

    def toggleClock():
        global timeOn
        if timeOnTrigger.config('relief')[-1] == 'sunken':
            timeOnTrigger.config(relief="raised")
            timeOn=0
        else:
            timeOnTrigger.config(relief="sunken")
            timeOn=1
            runnable = clock_runner()
            runnable.start()
    timeOnTrigger = Button (top, text="Time In", relief="raised", command=toggleClock)
    timeOnTrigger.place(x=130, y=430, width=100, height=50)

    def plus10sec():
        global min
        global sec
        if ((sec + 10) >= 60):
            sec = (sec + 10) - 60
            min+=1
        else:
            sec+=10
        writeFile(output_file)
    plus10seconds = Button(top, text="+10 seconds", command=plus10sec).place(x=380, y=450, width=150, height=20)

    def minus10sec():
        global min
        global sec
        if ((sec - 10) < 0):
            sec = 60 + (sec - 10)
            min-=1
        else:
            sec-=10
        writeFile(output_file)
    minus10seconds = Button(top, text="-10 seconds", command=minus10sec).place(x=380, y=475, width=150, height=20)

    def plus1sec():
        global min
        global sec
        if ((sec + 1) >= 60):
            sec = (sec + 1) - 60
            min+=1
        else:
            sec+=1
        writeFile(output_file)
    plus1second = Button(top, text="+1 seconds", command=plus1sec).place(x=380, y=400, width=100, height=20)

    def minus1sec():
        global min
        global sec
        if ((sec - 1) < 0):
            sec = 60 + (sec - 1)
            min-=1
        else:
            sec-=1
        writeFile(output_file)
    minus1second = Button(top, text="-1 seconds", command=minus1sec).place(x=380, y=425, width=100, height=20)

    def plustenthsec():
        global min
        global sec
        global tenth
        if ((tenth + 1) > 9):
            tenth = 0
            if ((sec + 1) >= 60):
                sec = 0
                min+=1
            else:
                sec += 1
        else:
            tenth+=1
        writeFile(output_file)
    plustenthsecond = Button(top, text="+0.1 seconds", command=plustenthsec).place(x=500, y=400, width=100, height=20)

    def minustenthsec():
        global min
        global sec
        global tenth
        if ((tenth - 1) < 0):
            tenth = 9
            if ((sec - 1) < 0):
                sec = 59
                min-=1
            else:
                sec -= 1
        else:
            tenth-=1
        writeFile(output_file)
    minustenthsecond = Button(top, text="-0.1 seconds", command=minustenthsec).place(x=500, y=425, width=100, height=20)

    minInput = Entry(top, text="8")
    minInput.place(x=130, y=400, width=50, height=20)
    secInput = Entry(top, text="00")
    secInput.place(x=205, y=400, width=50, height=20)
    tenthInput = Entry(top, text="0")
    tenthInput.place(x=280, y=400, width=50, height=20)
    colon = Label(top, text=":").place(x=190, y=400, width=10, height=20)
    decimal = Label(top, text=".").place(x=265, y=400, width=10, height=20)
    def update_time():
        global min
        global sec
        global tenth
        min=int(minInput.get())
        sec=int(secInput.get())
        tenth=int(tenthInput.get())
        writeFile(output_file)
    update_timer = Button (top, text="Update", command=update_time).place(x=260, y=450, width=100, height=20)

    HeaderLabel = Label(top, text="Header").place(x=600, y=10, width=450, height=20)
    customHeaderLabel = Label(top, text="Enter a Custom Header Here:").place(x=600, y=40,width=450,height=20)
    customHeadervalue = StringVar()
    customHeadervalue.set("Enter a Custom Header")
    customHeader = Entry(top, textvariable=customHeadervalue)
    customHeader.place(x=600, y=70,width=450,height=20)
    customHeadervalue.trace('w', lambda name, index, mode, sv=customHeadervalue: writeFile(output_file))
    hpointsPerQuarterLabel.set(homeName.get()+" Points Per Quarter: 1st-" + str(hscore[0]) + " | 2nd-" + str(hscore[1]) + " | 3rd-" + str(hscore[2]) + " | 4th-" + str(hscore[3]))
    hpointsPerQuarter = Radiobutton(top, textvariable=hpointsPerQuarterLabel, value = 1, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=100,width=450,height=20)
    vpointsPerQuarterLabel.set(visitorName.get()+" Points Per Quarter: 1st-" + str(vscore[0]) + " | 2nd-" + str(vscore[1]) + " | 3rd-" + str(vscore[2]) + " | 4th-" + str(vscore[3]))
    vpointsPerQuarter = Radiobutton(top, textvariable=vpointsPerQuarterLabel, value = 2, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=130,width=450,height=20)
    customHeader = Radiobutton(top, textvariable=customHeadervalue, value=3, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=160,width=450,height=20)
    blankHeader = Radiobutton(top, text="Blank", value=4, variable=selected_header, command=lambda: writeFile(output_file)).place(x=600, y=190,width=450,height=20)

    FooterLabel = Label(top, text="Footer").place(x=600, y=250, width=450, height=20)
    customFooterLabel = Label(top, text="Enter a Custom Footer Here:").place(x=600, y=280,width=450,height=20)
    customFootervalue = StringVar()
    customFootervalue.set("Enter a Custom Footer")
    customFooter = Entry(top, textvariable=customFootervalue)
    customFooter.place(x=600, y=310,width=450,height=20)
    customFootervalue.trace('w', lambda name, index, mode, sv=customFootervalue: writeFile(output_file))
    
    hfpointsPerQuarter = Radiobutton(top, textvariable=hpointsPerQuarterLabel, value = 1, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=340,width=450,height=20)
    vfpointsPerQuarter = Radiobutton(top, textvariable=vpointsPerQuarterLabel, value = 2, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=370,width=450,height=20)
    customFooter = Radiobutton(top, textvariable=customFootervalue, value=3, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=400,width=450,height=20)
    blankFooter = Radiobutton(top, text="Blank", value=4, variable=selected_footer, command=lambda: writeFile(output_file)).place(x=600, y=430,width=450,height=20)
    selected_footer.set(4)
    selected_header.set(4)


top.protocol("WM_DELETE_WINDOW", on_closing)
top.bind('<Escape>', exit)
top.protocol("WM_DELETE_WINDOW", on_closing)
top.mainloop()
