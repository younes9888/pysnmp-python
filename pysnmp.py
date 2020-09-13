import datetime
import tkinter as ttk
from time import sleep
from tkinter import messagebox, scrolledtext
import winsound
from random import randint
from pysnmp.hlapi.twisted.cmdgen import lcd
import threading
from pysnmp.hlapi import *



window = ttk.Tk()
# window.state('zoomed')
# window.resizable(False,False)
window.geometry('1300x820')
window.title('Modulators Monitoring System')
window.iconbitmap('modulator.ico')
window.configure(background='#828271')
list1 = []
list2 = []
list3 = []
list4 = []
system_uptime = '1.3.6.1.4.1.5835.5.2.100.1.9.5.0'
output_level = '1.3.6.1.4.1.5835.5.2.1000.1.33.0'
temperature = '1.3.6.1.4.1.5835.5.2.100.1.9.1.0'
redundancy = '1.3.6.1.4.1.5835.5.2.1800.1.3.0'
temperature1 = ''
temperature2 = ''
temperature3 = ''
temperature4 = ''
cm_color1 = ''
cm_color2 = ''
cm_color3 = ''
cm_color4 = ''
m1redundancy = 0
m2redundancy = 0
m3redundancy = 0
m4redundancy = 0
text = ttk.StringVar()
text.set("Alarm is enable")
x = True
sound = 'on'
photo1 = ttk.PhotoImage(file='modulator.png')

opl1 = ttk.DoubleVar()
label1 = ttk.Label(window, text='Output level: ', font=12)
label1.place(x=31, y=123)
label11 = ttk.Label(window, textvariable=opl1, font=12)
label11.place(x=125, y=123)

opl2 = ttk.DoubleVar()
label2 = ttk.Label(window, text='Output level: ', font=12)
label2.place(x=31, y=253)
label22 = ttk.Label(window, textvariable=opl2, font=12)
label22.place(x=125, y=253)

opl3 = ttk.DoubleVar()
label3 = ttk.Label(window, text='Output level: ', font=12)
label3.place(x=31, y=383)
label33 = ttk.Label(window, textvariable=opl3, font=12)
label33.place(x=125, y=383)

opl4 = ttk.DoubleVar()
label4 = ttk.Label(window, text='Output level: ', font=12)
label4.place(x=31, y=513)
label44 = ttk.Label(window, textvariable=opl4, font=12)
label44.place(x=125, y=513)

ctemperature = ttk.Canvas(height=20, width=170, bg="white")
ctemperature.place(x=920, y=15)
ctemperature.create_text(4, 3, anchor=ttk.NW, text='Temperature (Celsius)', font=22)

cm1 = ttk.Canvas(height=90, width=490, bg='white')
cm1.create_image(0, 0, anchor=ttk.NW, image=photo1)
cm1.create_text(4, 3, anchor=ttk.NW, text='Modulator-1', font=17)
cm1.place(x=30, y=30)

carrow = ttk.Canvas(height=120, width=150, bg='#828271', highlightthickness=0)
carrow.place(x=525, y=70)
felche = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
blink_boolean1 = True

cm2 = ttk.Canvas(height=90, width=490, bg='white')
cm2.create_image(0, 0, anchor=ttk.NW, image=photo1)
cm2.create_text(4, 3, anchor=ttk.NW, text='Modulator-2', font=17)
cm2.place(x=30, y=160)
carrow2 = ttk.Canvas(height=120, width=150, bg='#828271', highlightthickness=0)
carrow2.place(x=525, y=190)
felche2 = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
blink_boolean2 = True

cm3 = ttk.Canvas(height=90, width=490, bg='white')
cm3.create_image(0, 0, anchor=ttk.NW, image=photo1)
cm3.create_text(4, 3, anchor=ttk.NW, text='Modulator-3', font=17)
cm3.place(x=30, y=290)
carrow3 = ttk.Canvas(height=120, width=150, bg='#828271', highlightthickness=0)
carrow3.place(x=525, y=310)
felche3 = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
blink_boolean3 = True

cm4 = ttk.Canvas(height=90, width=490, bg='white')
cm4.create_image(0, 0, anchor=ttk.NW, image=photo1)
cm4.create_text(4, 3, anchor=ttk.NW, text='Modulator-4', font=17)
cm4.place(x=30, y=420)
carrow4 = ttk.Canvas(height=120, width=150, bg='#828271', highlightthickness=0)
carrow4.place(x=525, y=430)
felche4 = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
blink_boolean4 = True

try:
    f = open('settings.txt', "r")
    lines = f.readlines()
    ip_m1 = str(lines[0])
    ip_m2 = str(lines[1])
    ip_m3 = str(lines[2])
    ip_m4 = str(lines[3])
    port = int(lines[4])
    temperature_threshold = int(lines[5])
    f.close()
except:
    ttk.messagebox.showerror(title='Error lunching the application', message='an error has occurred')

textbox = ttk.scrolledtext.ScrolledText(window, undo=True, width=90, height=5, state='disabled')
textbox['font'] = ('consolas', '12')
textbox.place(x=26, y=550)
textbox_boolean1 = True
textbox_boolean2 = True
textbox_boolean3 = True
textbox_boolean4 = True


data = (
  ObjectType(ObjectIdentity('1.3.6.1.4.1.5835.5.2.100.1.9.0')),
ObjectType(ObjectIdentity('1.3.6.1.4.1.5835.5.2.1800.1.33')),
ObjectType(ObjectIdentity('1.3.6.1.4.1.5835.5.2.1000.1.3'))
)
from pysnmp.hlapi.lcd import CommandGeneratorLcdConfigurator
def getdata_m1():
    global blink_boolean1, felche, carrow, textbox_boolean1
    temcolor = ''
    output_level1 = 0.0
    try:
        g = getCmd(SnmpEngine()
                   , CommunityData('public', mpModel=1)
                   , UdpTransportTarget(('10.118.27.37', 161))
                   , ContextData()
                   , *data)

        errorIndication, errorStatus, errorIndex, varBinds = next(g)

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
                  )
        else:
            for name, varBind in varBinds:
                list1.append(str(varBind))


        temperature1 = list1[0]
        m1redundancy = list1[1]
        output_level1 = (float(list1[2]) / 10)
    except:
        ttk.messagebox.showerror(title='Error', message='an error has been occurred with Modulator-1')
    
    opl1.set(output_level1)
    if int(m1redundancy) == 0:
        cm_color1 = 'lightgreen'
        cm1.config(bg=cm_color1)
        carrow.delete(felche)
        blink_boolean1 = False
        textbox_boolean1 = True
    else:
        cm_color1 = 'tomato'
        cm1.config(bg=cm_color1)
        blink_boolean1 = True
        blink()
        if sound == 'on':
            playsound()
        else:
            sleep(1)
        if textbox_boolean1 == True:
            textbox.config(state='normal')
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            textbox.insert(ttk.END, str(now) + ": Modulator-1 switched from main to backup\n")
            textbox_boolean1 = False
            textbox.config(state='disabled')

    if int(temperature1) > 0 and int(temperature1) < 40:
        temcolor = 'green'
    elif int(temperature1) > 39 and int(temperature1) < 50:
        temcolor = 'orange'
    elif int(temperature1) > 49:
        temcolor = 'red'

    tm1 = ttk.Canvas(height=20, width=404, bg="white")
    tm1.place(x=800, y=70)
    n1 = 0
    for i in range(0, int(temperature1)):
        tm1.create_rectangle((n1, 1, 4 + n1, 20), fill=temcolor, width=0)
        tm1.create_text(200, 10, text=str(temperature1) + '°', fill='black', font=22)
        n1 = n1 + 4
    tm1.update()
    if int(temperature1) >= temperature_threshold and sound == 'on':
        playsound()
    list1.clear()
    threading.Timer(4, getdata_m1).start()
    


def soundControl():
    global x
    global sound
    if x == True:
        x = False
        text.set("Alarm is disabled")
        sound = 'off'
    else:
        x = True
        text.set("Alarm is enabled")
        sound = 'on'
def playsound():
    winsound.Beep(2000, 1000)
    sleep(1)
def blink():
    global blink_boolean1, felche, carrow
    carrow.delete(felche)
    if blink_boolean1 == True:
        felche = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='red', width=15)
        carrow.after(500, stopblink)
def stopblink():
    global blink_boolean1, felche, carrow
    carrow.delete(felche)
    if blink_boolean1 == True:
        felche = carrow.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
        carrow.after(500, blink)
def blink2():
    global blink_boolean2, felche2, carrow2
    carrow2.delete(felche2)
    if blink_boolean2 == True:
        felche2 = carrow2.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='red', width=15)
        carrow2.after(500, stopblink2)
def stopblink2():
    global blink_boolean2, felche2, carrow2
    carrow2.delete(felche2)
    if blink_boolean2 == True:
        felche2 = carrow2.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
        carrow2.after(500, blink2)
def blink3():
    global blink_boolean3, felche3, carrow3
    carrow3.delete(felche3)
    if blink_boolean3 == True:
        felche3 = carrow3.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='red', width=15)
        carrow3.after(500, stopblink3)
def stopblink3():
    global blink_boolean3, felche3, carrow3
    carrow3.delete(felche3)
    if blink_boolean3 == True:
        felche3 = carrow3.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
        carrow3.after(500, blink3)
def blink4():
    global blink_boolean4, felche4, carrow4
    carrow4.delete(felche4)
    if blink_boolean4 == True:
        felche4 = carrow4.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='red', width=15)
        carrow4.after(500, stopblink4)
def stopblink4():
    global blink_boolean4, felche4, carrow4
    carrow4.delete(felche4)
    if blink_boolean4 == True:
        felche4 = carrow4.create_line(10, 10, 60, 10, arrow=ttk.FIRST, fill='#828271')
        carrow4.after(500, blink4)
def clearlog():
    textbox.config(state='normal')
    textbox.delete("1.0", ttk.END)
    textbox.config(state='disabled')

but1 = ttk.Button(window, textvariable=text, font=16, command=soundControl).place(x=1090, y=550)
but2 = ttk.Button(window, text='Clear events log', font=16, command=clearlog).place(x=1090, y=595)

getdata_m1()
window.mainloop()
