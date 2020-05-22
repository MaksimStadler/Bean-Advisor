# import required libraries
import tkinter.ttk as ttk
from datetime import *
from requests import *
from tkinter import *
import time

tk = Tk

# set colour variables
grey1 = '#111111'
grey2 = '#333333'
grey3 = '#555555'
grey4 = '#777777'
text1 = '#bbbbbb'
text2 = '#999999'


# define splash screen
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
        height = 500
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.resizable(False, False)

        # set window title, icon, etc.
        self.title('Bean Advisor')
        self.iconbitmap(default='bean_advisor_icon.ico')
        self.configure(background=grey1)

        # define window content
        text = 'Press button for your recommended dose of  b e a n.'
        instructions = Label(self, font=('Calibri', 13), bg=grey2, fg=text1,
                             text=text)
        instructions.place(relx=0.02, rely=0.015, relwidth=0.96,
                           relheight=0.075)

        bean_button = Button(self, text='PRESS FOR BEANS', font=('Calibri', 22),
                             activebackground=grey3, activeforeground=text1,
                             disabledforeground=text2, bg=grey2, fg=text1,
                             relief='flat',
                             borderwidth=0)
        bean_button.place(relx=0.02, rely=0.105, relwidth=0.96,
                          relheight=0.075)

        bean = PhotoImage(file='Bean Advisor Logo (Small).png')
        display = Label(self, text='BEAN', image=bean, font=('Calibri', 10),
                        bg=grey2, fg=text1)
        display.place(relx=0.02, rely=0.195, relwidth=0.96, relheight=0.6)

        bean_info = Label(self, text='', font=('Calibri', 10), bg=grey2,
                          fg=text1)
        bean_info.place(relx=0.02, rely=0.81, relwidth=0.96, relheight=0.075)

        progress_info = Label(self, text='', font=('Calibri', 10), bg=grey2,
                              fg=text1)
        progress_info.place(relx=0.02, rely=0.9, relwidth=0.96,
                            relheight=0.04)

        ttk.Style().theme_use('classic')
        ttk.Style().configure('blue.Horizontal.TProgressbar',
                              background='#007fff',
                              foreground=grey4,
                              troughcolor=grey1,
                              relief='flat',
                              troughrelief='flat',
                              borderwidth=0)
        progress_bar = ttk.Progressbar(self, orient=HORIZONTAL,
                                       mode='determinate',
                                       style='blue.Horizontal.TProgressbar')

        progress_bar['value'] = 20
        progress_bar.place(relx=0.02, rely=0.94, relwidth=0.96,
                           relheight=0.04)

        # terminate splash screen
        # simulate a delay while loading
        time.sleep(2)

        # finished loading so destroy splash
        splash.destroy()

        # show window again
        self.deiconify()

    # def bean_update(self):


BeanApp().mainloop()
