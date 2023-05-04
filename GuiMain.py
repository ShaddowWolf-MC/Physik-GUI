import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
import serial
import serial.tools.list_ports
import sys
import time
import threading
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


comport = '1'
baudrate = 0
arduinoDataPassFrame = []
arduinoDataPassFrame.append(serial.Serial())
#First row is Time
#Second row is Round
dataTable = np.zeros(130, 130)
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
                                            commentBaudrate.grid_forget(), self.checkbox.grid_forget(), 
                                            self.text1.grid(row=1, column=1, padx=5), self.text2.grid(row=1, column=2, padx=5),
                                            self.buildGUInew()])
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
        self.checkbox = tk.Checkbutton(self.window, text='Disable Serial connection \n for Debugging',variable=self.checkVar)
        self.checkbox.grid(row=2, column=1, padx=60)

        



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


    def buildGUInew(self):
        time.sleep(1)
        self.checkbox.grid(row=1, column=1, padx=100)



def setupArduino():
    
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    print("Connected COM ports: " + str(connected))
    #get all conected com ports

    arduinoData = serial.Serial(comport, baudrate)
    time.sleep(1)
    DataFetcher()

def passArduinoObj(arduinoData):
    print(arduinoData)
    arduinoDataPassFrame.append(arduinoData)



class DataFetcher:
    arduinoData1 = arduinoDataPassFrame[0] # pylint:disable=invalid-name,used-before-assignment,undefined-variable

    def __init__(self):
        t = threading.Thread(target=self.fetchData)
        t.start()
        print("Thread Started")


    def fetchData(self):
        self.handShake()
        while True:
            while (arduinoData1.inWaiting() == 0): # pylint:disable=invalid-name,used-before-assignment,undefined-variable
                #E
                pass
            dataPacket = arduinoData1.readline()
            dataPacket = str(dataPacket, 'utf-8')
            dataPacket = dataPacket.strip('\r\n')
            workPiece = dataPacket.split(":")
            #First part is Sensor, Second is Time, Third is Round
            if(workPiece[1].isdigit):
                dataTable[workPiece[1]][workPiece[3]] = workPiece[2] 
            print(dataPacket)

    def handShake(self):
        stayInLoop = True
        cmd1 = "C"
        cmd1=cmd1+'\r'
        arduinoData1.write(cmd1.encode())
        while stayInLoop:
            while arduinoData1.inWaiting() == 0:
                pass
            dataPacket = arduinoData1.readline()
            dataPacket = str(dataPacket, 'utf-8')
            dataPacket = dataPacket.strip('\r\n')
            if("C" in dataPacket):
                cmd2 = "R"
                cmd2=cmd2+'\r'
                arduinoData1.write(cmd2.encode())
                stayInLoop = False





        
    
#bool handshake(){
#  bool hasfinished1, hasfinished2 = false;
#  string recive1, recive2;
#  while(hasfinished1 != true){
#    if(Serial.available() != 0){
#      recive1 = Serial.readStringUntil('\r');
#      if(recive1 != "C"){
#      }
#      else{
#        Serial.println('C');
#        hasfinished1 = true;
#        unsigned long currentMillis = millis();  // get the current time
#        if (currentMillis - previousMillis >= intervalHandshake) {
#          previousMillis = currentMillis;  // update the previous time
#        }
#      }
#    }
#  }
#  while(hasfinished2 != true){
#    if(Serial.available() != 0){
#      recive2 = Serial.readStringUntil('\r');
#     if(recive2 != "R"){
#     }
#      else{
#        hasfinished2 = true;
#        unsigned long currentMillis = millis();  // get the current time
#        if (currentMillis - previousMillis >= intervalHandshake) {
#          previousMillis = currentMillis;  // update the previous time
#        }
#        return true;
#      }
#    }
#  }
#}


            




MyGUI()
print("Testlol")
#calls class to run programm

