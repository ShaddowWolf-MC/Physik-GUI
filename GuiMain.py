import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
import serial
import serial.tools.list_ports
import sys



#arduinoData = serial.Serial('com3')

print("TKinter Version", tk.TkVersion)
print("Python Version", sys.version)
#Testdata to confirm working code

class MyGUI:
    def __init__(self):
        
        self.window = tk.Tk()
        self.window.minsize(500, 500)


        comlist = serial.tools.list_ports.comports()
        connected = []
        for element in comlist:
            connected.append(element.device)
        print("Connected COM ports: " + str(connected))

        defaultComDD = StringVar(self.window)
        defaultComDD.set("Choose COMport")

        defaultBaudrateDD = StringVar(self.window)
        defaultBaudrateDD.set("Choose Baudrate")
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


        btn1 = tk.Button(layoutframe, text='1', font=('Arial', 20))
        btn1.grid(row=0, column=0, sticky=tk.W)
        
        dropdown1 = tk.OptionMenu(self.window, defaultComDD, *comlist)
        dropdown1.grid(row=2, column=2, padx=60)

        dropdown2 = tk.OptionMenu(self.window, defaultBaudrateDD, *baudrates)
        dropdown2.grid(row=2, column=5, padx=40)

        commentBaudrate = tk.Label(self.window, text="Baudrate must be same as \n configured in Arduino code \n\n" 
                                   "If unknown, use 115200!", font=('Calibre', 10))
        commentBaudrate.grid(row=3, column=5, padx=40)

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

    def show_message(self):
        if self.check_state.get() == 0:
            #when starting in the beginning of the Textbox we need index 1 as a string, and index to as the end
            #also: the index starts at 1, why???
            print(self.textbox.get('1.0', tk.END)) 
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))
    


    #def setBitrate(self):








MyGUI()
#calls class to run programm