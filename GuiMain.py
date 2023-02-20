import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
import serial
import serial.tools.list_ports
import sys


baudrate = 115200
comport = 'com1'
#arduinoData = serial.Serial('com3')

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

        self.showDropdowns = tk.BooleanVar(self.window)
        self.showDropdowns = True

        layoutframe = tk.Frame(self.window)
        layoutframe.columnconfigure(0, weight=1, uniform='sixth')
        layoutframe.columnconfigure(1, weight=1, uniform='sixth')
        layoutframe.columnconfigure(2, weight=1, uniform='sixth')
        layoutframe.columnconfigure(3, weight=1, uniform='sixth')
        layoutframe.columnconfigure(4, weight=1, uniform='sixth')
        layoutframe.columnconfigure(5, weight=1, uniform='sixth')
        #colums for my gui, will utilise later


        btn1 = tk.Button(self.window, text='Set Port / baudrate', font=('Arial', 13),
                          command= lambda: [self.setValues(), self.dropdown1.grid_forget(), self.dropdown2.grid_forget(),
                                            self.text1.grid(row=2, column=2, padx=60), self.text2.grid(row=2, column=4, padx=40)])
        btn1.grid(row=2, column=5)
        


        self.dropdown1 = tk.OptionMenu(self.window, self.defaultComDD, *comlist)
        self.dropdown1.grid(row=2, column=2, padx=60)
        #dropdown for choosing the comport
        
        self.portText = "Value fetching failed"
        self.baudText = "Value fetching failed"


        self.text1 = tk.Label(self.window, text= self.portText)
        self.text2 = tk.Label(self.window, text=("Baudrate = ", baudrate))
        

        self.dropdown2 = tk.OptionMenu(self.window, self.defaultBaudrateDD, *baudrates)
        self.dropdown2.grid(row=2, column=4, padx=40)
        #dropdown for choosing the baudrate

        commentBaudrate = tk.Label(self.window, text="Baudrate must be same as \n configured in Arduino code \n\n" 
                                   "If unknown, use 115200!", font=('Calibre', 10))
        commentBaudrate.grid(row=3, column=5, padx=40)



        str_out=tk.StringVar(self.window)
        str_out.set("Output")


        #layoutframe.pack(fill='x')

        #self.label = tk.Label(self.window, text="Your Message", font=('Arial', 18))
        # self.label.pack(padx=10, pady=12)

        # self.textbox = tk.Text(self.window, height=5, font=('Arial', 15))
        # self.textbox.pack(padx=10, pady=10)


        # self.check_state = tk.IntVar()
        # self.check = tk.Checkbutton(self.window, text="Show Messagebox", font=('Arial', 13), variable=self.check_state)
        # self.check.pack(padx=10, pady=10)

        # self.button = tk.Button(self.window, text="Show message", font=('Arial', 13), command=self.show_message)
        # self.button.pack(padx=10, pady=10)
        



        self.window.mainloop()

    def setValues(self):
        #self.str_out.set(self.defaultComDD.get())
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
        setupArduino()        


    def show_message(self):
        if self.check_state.get() == 0:
            #when starting in the beginning of the Textbox we need index 1 as a string, and index to as the end
            #also: the index starts at 1, why???
            print(self.textbox.get('1.0', tk.END)) 
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))
    


    #def setBitrate(self):

def setupArduino():
    arduinoData = serial.Serial(comport)







MyGUI()
#calls class to run programm