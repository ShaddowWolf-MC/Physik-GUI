import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
import serial
import serial.tools.list_ports
import sys
import time
import threading



baudrate = 115200
comport = 'com1'
arduinoData = serial.Serial(comport, baudrate)

print("TKinter Version", tk.TkVersion)
print("Python Version", sys.version)
#Testdata to confirm working code

class MyGUI:
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.minsize(500, 500)
        self.window.title("Physics GUI Window - Dev_Version")
        #Set window, window size and window title


        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        print("Connected COM ports: " + str(connected))
        #get all conected com ports


        self.defaultComDD = tk.StringVar(self.window)
        self.defaultComDD.set("Choose COMport")
        #string for Dropdown menu
        #self because otherwise it doesnt work, idk why?

        self.defaultBaudrateDD = StringVar(self.window)
        self.defaultBaudrateDD.set("Choose Baudrate")
        baudrates = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200]
        #Possible baudrates for the Arduino, should usually be 115200



        layoutframe = tk.Frame(self.window)
        layoutframe.columnconfigure(0, weight=1, uniform='sixth')
        layoutframe.columnconfigure(1, weight=1, uniform='sixth')
        layoutframe.columnconfigure(2, weight=1, uniform='sixth')
        layoutframe.columnconfigure(3, weight=1, uniform='sixth')
        layoutframe.columnconfigure(4, weight=1, uniform='sixth')
        layoutframe.columnconfigure(5, weight=1, uniform='sixth')
        #colums for my gui, will utilise later


        btn1 = tk.Button(self.window, text='Set Port / baudrate', font=('Arial', 13),
                          command= lambda: [self.setValues(), self.dropdown1.grid_forget(), self.dropdown2.grid_forget(), btn1.grid_forget(), 
                                            commentBaudrate.grid_forget(), self.c1.grid_forget(), 
                                            self.text1.grid(row=1, column=1, padx=5), self.text2.grid(row=1, column=2, padx=5)])
        btn1.grid(row=2, column=5, padx=60)
        #button that removes the dropdowns, sets the arduino conection and adds the lables


        self.dropdown1 = tk.OptionMenu(self.window, self.defaultComDD, *comlist)
        self.dropdown1.grid(row=2, column=2, padx=60)
        #dropdown for choosing the comport
        
        self.portText = "Value fetching failed"
        self.baudText = "Value fetching failed"
        #two strings for the lables below

        self.text1 = tk.Label(self.window, text= self.portText, font=('Calibre', 8))
        self.text2 = tk.Label(self.window, text=("Baudrate = ", baudrate), font=('Calibre', 8))
        #texts to replace the dropdown menus after the baudrate / port is choosen

        self.dropdown2 = tk.OptionMenu(self.window, self.defaultBaudrateDD, *baudrates)
        self.dropdown2.grid(row=2, column=4, padx=40)
        #dropdown for choosing the baudrate

        commentBaudrate = tk.Label(self.window, text="Baudrate must be same as \n configured in Arduino code \n\n" 
                                   "If unknown, use 115200!", font=('Calibre', 10))
        commentBaudrate.grid(row=3, column=4, padx=40)
        #comment for choosing the baudrate

        self.checkVar = tk.IntVar()
        self.c1 = tk.Checkbutton(self.window, text='Disable Serial connection \n for Debugging',variable=self.checkVar)
        self.c1.grid(row=2, column=1, padx=60)

        



        self.window.mainloop()

    def setValues(self):
        print(self.defaultComDD.get())
        comport = self.defaultComDD.get()
        print(comport)
        print(self.defaultBaudrateDD.get())
        baudrate = self.defaultBaudrateDD.get()
        print(baudrate)
        #Changes the value of defaultComDD and defaultBaudrateDD to the selected values
    
        comport = self.defaultComDD.get().removesuffix("- Kommunikationsanschluss (COM1)") 
        self.text1['text'] = "Port = " + comport 
        self.text2['text'] = "Baudrate = " + self.defaultBaudrateDD.get()
        #changes buttons to text lables

        if self.checkVar.get() == 0:
            print("Unchecked")
            setupArduino()  
        else:
            print("Checked")
        #functionallity for out Debug button


    #def setBitrate(self):

def setupArduino():
    arduinoData = serial.Serial(comport, baudrate)
    time.sleep(1)
    DataFetcher()


class DataFetcher:

    def fetchData(self):
        while True:
            while (arduinoData.inWaiting() == 0):
                #E
                pass
            dataPacket = arduinoData.readline()
            dataPacket = str(dataPacket, 'utf-8')
            dataPacket = dataPacket.strip('\r\n')
            print(dataPacket)

    def __init__(self):
        t = threading.Thread(target=self.fetchData)
        t.start()

            




MyGUI()
print("Testlol")
#calls class to run programm

