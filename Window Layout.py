# import required libraries
from datetime import *
from requests import *
from tkinter import *
import pandas as pd
from bs4 import *
import time

tk = Tk

# set colour variables
grey1 = '#222222'
grey2 = '#333333'
grey3 = '#444444'
grey4 = '#555555'
text1 = '#aaaaaa'
text2 = '#777777'


# defien splash screen
class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        # define window geometry
        width = 800
        height = 450
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.overrideredirect(True)

        # define content
        bean_logo = PhotoImage(file='bean_advisor_logo.png')
        splash_image = Label(self, bg=grey2, image=bean_logo)
        splash_image.place(relwidth=1, relheight=1)

        # required to make window show before the program gets to the mainloop
        self.update()


class BeanApp(tk):
    def __init__(self):
        tk.__init__(self)

        # display splash screen

        self.withdraw()
        splash = Splash(self)

        # set window size and position on screen
        width = 400
        height = 600
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False, False)

        # set window title, icon, etc.
        self.title('Bean Advisor')
        self.iconbitmap(default='bean_advisor_icon.ico')
        self.configure(background=grey2)

        # define window features

        # terminate splash screen
        # simulate a delay while loading
        time.sleep(2)

        # finished loading so destroy splash
        splash.destroy()

        # show window again
        self.deiconify()


BeanApp().mainloop()
