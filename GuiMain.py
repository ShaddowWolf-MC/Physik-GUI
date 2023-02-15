import tkinter as tk
from tkinter import messagebox
import sys


print("TKinter Version", tk.TkVersion)
print("Python Version", sys.version)


class MyGUI:
    def __init__(self):
        
        self.window = tk.Tk()

        layoutframe = tk.Frame(self.window)
        layoutframe.columnconfigure(0, weight=1)
        layoutframe.columnconfigure(1, weight=1)
        layoutframe.columnconfigure(2, weight=1)
        layoutframe.columnconfigure(3, weight=1)
        layoutframe.columnconfigure(4, weight=1)
        layoutframe.columnconfigure(5, weight=1)

        btn1 = tk.Button(layoutframe, text='1', font=('Arial', 20))
        btn1.grid(row=0, column=0, sticky=tk.W)
        

        layoutframe.pack(fill='x')

        self.label = tk.Label(self.window, text="Your Message", font=('Arial', 18))
        self.label.pack(padx=10, pady=12)

        self.textbox = tk.Text(self.window, height=5, font=('Arial', 15))
        self.textbox.pack(padx=10, pady=10)


        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.window, text="Show Messagebox", font=('Arial', 13), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.window, text="Show message", font=('Arial', 13), command=self.show_message)
        self.button.pack(padx=10, pady=10)




        self.window.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            #when starting in the beginning of the Textbox we need index 1 as a string, and index to as the end
            #also: the index starts at fucking 1, why???
            print(self.textbox.get('1.0', tk.END)) 
        else:
            messagebox.showinfo(title="Message", message=self.textbox.get('1.0', tk.END))

MyGUI()
