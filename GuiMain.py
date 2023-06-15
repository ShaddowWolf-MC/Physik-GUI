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
from matplotlib.figure import Figure
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import seaborn as sns


#Testdata & Implementory data start
comport = 'Com5'
baudrate = 115200
arduinoData = serial.Serial(comport, baudrate)
#XAxis row is Sensor
#Yaxis row is Time
dataTable = np.zeros((13, 130))
dataTableTestData = np.zeros((13, 130))
print("TKinter Version", tk.TkVersion)
print("Python Version", sys.version)
activeAtLine = 0
lastWrittenSensor = 0
#Colours for the lables for graph lines
colors = ['red', 'green', 'blue', 'orange', 'purple']
#Testdata to confirm working code ends here

class MyGUI:
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.minsize(900, 600)
        self.window.title("Physics GUI Window - Dev_Version")
        #Set window, window size and window title

        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        print("Connected COM ports: " + str(connected))
        #get all conected com ports

        #Create figure object for graph later + axes obj
        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)


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
                                            commentBaudrate.grid_forget(), self.checkbox.grid_forget(), self.buildGUInew()])
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

        


        self.update_plot()
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
        #self.generateTestdata() 
        self.text1.grid(row=1, column=1, padx=100)
        self.text2.grid(row=1, column=2, padx=100)
        #self.checkbox.grid(row=1, column=1, padx=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=4, column=1, sticky='nsew')

    def update_data(self, dataTable):
        # Update the plot data
        self.ax.clear()
        #Set back to dataTable later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.ax.plot(dataTable)
        for i in range(16):
            color = colors[i % len(colors)]
            self.ax.plot(dataTable[:,i], color=color)

            # Create a label widget for the current graph and add it to the Tkinter window
            self.label = tk.Label(self.window, text=f'Graph {i}', bg=color)
            self.label.grid(row=i+1, column=0, sticky='w')

        self.ax.set_xlabel("Sensor")
        self.ax.set_ylabel("Zeit bei Sensor")

    # Create a function that updates the plot
    def update_plot(self):
        # Update the plot data
        self.update_data(dataTable)

        # Redraw the plot
        self.fig.canvas.draw()
        self.fig.tight_layout()

        # Schedule the update function to run again in 1 second
        self.window.after(1000, self.update_plot)

    def generateTestdata(self):
        for i in range(1, 10):
            for j in range(1,11):
                dataTableTestData[j][i] = np.random.randint(0, 15)




def setupArduino():
    
    comlist = serial.tools.list_ports.comports()
    connected = []
    for element in comlist:
        connected.append(element.device)
    print("Connected COM ports: " + str(connected))
    #get all conected com ports
    time.sleep(1)
    DataFetcher()

#def passArduinoObj(arduinoData):
    #print(arduinoData)
    #arduinoDataPassFrame.append(arduinoData)



class DataFetcher:
    #comport = 'Com5'
    #baudrate = 115200
    #arduinoData = serial.Serial(comport, baudrate) # pylint:disable=invalid-name,used-before-assignment,undefined-variable

    def __init__(self):
        t = threading.Thread(target=self.fetchData)
        t.start()
        print("Thread Started")


    def fetchData(self):
        #arduinoData1 = arduinoDataPassFrame[0]\
        
        #self.handShake()
        while True:
            while (arduinoData.inWaiting() == 0): # pylint:disable=invalid-name,used-before-assignment,undefined-variable
                #E
                pass
            dataPacket = arduinoData.readline()
            dataPacket = str(dataPacket, 'utf-8')
            dataPacket = dataPacket.strip('\r\n')
            workPiece = dataPacket.split(":")
            workPiece[0].strip(":")
            workPiece[1].strip(":")
            workPiece[2].strip(":")
            print(workPiece[0])
            print(workPiece[1])
            print(workPiece[2])

            #First part is Sensor, Second is Round, Third is Time
            if(workPiece[0].isdigit and workPiece[1].isdigit and workPiece[2].isdigit):
                dataToWrite = float(workPiece[2])
                dataTable[int(workPiece[0])][int(workPiece[1])] = dataToWrite/1000
                activeAtLine = int(workPiece[2])
                lastWrittenSensor = int(workPiece[0])
            print(dataPacket)

    def handShake(self):
        comport = 'Com5'
        baudrate = 115200
        arduinoData = serial.Serial(comport, baudrate)
        stayInLoop = True
        cmd1 = "C"
        cmd1=cmd1+'\r'
        arduinoData.write(cmd1.encode())
        while stayInLoop:
            while arduinoData.inWaiting() == 0:
                pass
            dataPacket = arduinoData.readline()
            dataPacket = str(dataPacket, 'utf-8')
            dataPacket = dataPacket.strip('\r\n')
            if("C" in dataPacket):
                cmd2 = "R"
                cmd2=cmd2+'\r'
                arduinoData.write(cmd2.encode())
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

