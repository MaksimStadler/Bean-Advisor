'''
Program that tells you an edible variety of bean to eat based on the 'weather',
and how many of said bean to eat according to the date and temperature.

Splash screen code modified from James Kent on Stack Overflow
'''

# import required libraries
import PIL.Image as im
import PIL.ImageTk as itk
import tkinter.ttk as ttk
from datetime import *
from requests import *
from tkinter import *
import pandas as pd
import numpy as np
from bs4 import *
import pyglet
import time

# simplify tkinter
tk = Tk

# import fonts
pyglet.font.add_file('fonts/VoyaNui_1.15_0.ttf')
pyglet.font.add_file('fonts/DIN 1451 Mittelschrift Regular.ttf')
pyglet.font.add_file('fonts/DINLiA.ttf')

# set some variables
codeColumn = 'Code'
weather_dict = {}
weather_data = []

# set colour variables
grey1 = '#111111'
grey2 = '#333333'
grey3 = '#555555'
grey4 = '#777777'
text1 = '#bbbbbb'


# define required functions
def get_location():
    # Collect location/weather/time data
    location_url = 'https://ipinfo.io'

    location_data = eval(
        BeautifulSoup(get(location_url).text, 'lxml').select('p')[0].getText())
    global city, country, curr_time
    city = location_data['city'].upper()
    country = location_data['country'].upper()
    curr_time = datetime.now()


def load_file_data():
    global icao_lut, bean_lut, bean_list, cloud_lut, cloud_dict
    # load file data
    icao_lut = pd.read_csv('station_lut.csv')
    bean_lut = pd.read_csv('bean_lut.csv')
    bean_list = list(bean_lut['type'])
    cloud_lut = pd.read_csv('cloud_lut.csv')
    cloud_dict = cloud_lut.set_index('Code')['Value'].to_dict()


def get_weather():
    global weather_error
    try:
        # filter icao_lut based on country/city
        city_filter = icao_lut['City'].str.contains(city, na=False)
        country_filter = icao_lut['Country'] == country
        icao_list = list(icao_lut[country_filter][city_filter]['ICAO'])
        for icao in icao_list:
            weather_url = 'https://www.aviationweather.gov/metar/data?ids=' \
                          + icao
            global weather_data
            weather_data = BeautifulSoup(get(weather_url).text, 'lxml').select(
                'code')

            # test for available weather data and record first available string
            if weather_data:
                weather_data = weather_data[0].getText().split(' ')

                break

        weather_error = False

    except Exception:
        weather_error = True
        raise


def get_bean_data():
    global weather_error
    if weather_error:
        return 'Weather data not available.'
    # Determine Type of bean
    for code in weather_data:
        if 'KT' in code:
            weather_dict['windSpeed'] = int(code[-4:-2])
        elif code[:3] in cloud_dict and 'sky' not in weather_dict:
            weather_dict['sky'] = cloud_dict[code[:3]]
        elif '/' in code:
            weather_dict['temperature'] = int(
                code.split('/')[0].replace('M', '-'))
            break

    bean_value = (np.prod([weather_dict[k] for k in weather_dict]) / 2) % (
            len(bean_list) - 1)
    global bean_type
    bean_type = bean_list[int(bean_value)]

    # Determine quantity of bean
    bean_quantity = (curr_time.hour * curr_time.minute) % 60 + 1

    # Inform user or bean dose
    if bean_quantity == 1:
        return 'We recommend you consume {0} {1}.'.format(bean_quantity,
                                                          bean_type[:-1])
    return 'We recommend you consume {0} {1}.'.format(bean_quantity, bean_type)


# define window structure/initialize window
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
        icon = PhotoImage(file='Bean Advisor Logo (Bean).png')
        self.iconphoto(False, icon)
        self.configure(background=grey1)

        # define window content
        text = 'Press button for your recommended dose of b e a n.'
        self.instructions = Label(font=('DIN 1451 Mittelschrift', 13), bg=grey2,
                                  fg=text1, text=text)
        self.instructions.place(relx=0.015, rely=0.015, relwidth=0.97,
                                relheight=0.05)

        self.bean_button = Button(text='PRESS FOR BEANS', font=('Voya Nui', 22),
                                  command=lambda: self.bean_update(),
                                  activebackground=grey3,
                                  activeforeground=text1, bg=grey2, fg=text1,
                                  relief='flat', borderwidth=0,
                                  anchor='s', pady=5)
        self.bean_button.place(relx=0.015, rely=0.08, relwidth=0.97,
                               relheight=0.08)

        self.display = Label(text='BEAN', bg=grey2, fg=text1)
        image = im.open('Bean Advisor Logo (Small).png')
        image.thumbnail((300, 300))
        self.image = itk.PhotoImage(image)
        self.display.configure(image=self.image)
        self.display.place(relx=0.015, rely=0.175, relwidth=0.97, relheight=0.7)

        self.bean_info = Label(text='', font=('DIN 1451 Mittelschrift', 12),
                               bg=grey2, fg=text1)
        self.bean_info.place(relx=0.015, rely=0.89, relwidth=0.97,
                             relheight=0.055)

        ttk.Style().theme_use('classic')
        ttk.Style().configure('Horizontal.TProgressbar', background='#007fff',
                              troughcolor=grey2, relief='flat',
                              troughrelief='flat', borderwidth=0)
        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL,
                                            mode='determinate',
                                            style='Horizontal.TProgressbar')

        self.progress_bar.place(relx=0.015, rely=0.945, relwidth=0.97,
                                relheight=0.015)

        self.progress_info = Label(text='', font=('Courier New', 8), anchor='w',
                                   padx=-10, bg=grey1, fg=text1)
        self.progress_info.place(relx=0.01, rely=0.96, relwidth=0.97,
                                 relheight=0.03)

        # simulate a delay while loading
        time.sleep(1)

        # finished loading so destroy splash
        splash.destroy()

        # show window again
        self.deiconify()

    # animate progress bar and simulate delay
    def animate_progress(self, start, stop):
        for i in range(start, stop):
            self.progress_bar['value'] = i
            self.update_idletasks()
            time.sleep(0.01)

    # update bean data
    def bean_update(self):
        self.progress_info.configure(text='Processing request...')
        self.bean_info.config(text='Waiting for bean data...')
        image = im.open('Bean Advisor Logo (Small).png')
        image.thumbnail((300, 300))
        self.image = itk.PhotoImage(image)
        self.display.configure(image=self.image)
        self.update_idletasks()
        self.animate_progress(0, 20)
        self.progress_info.configure(text='Finding your location...')
        self.update_idletasks()
        get_location()
        self.animate_progress(20, 40)
        self.progress_info.configure(text='Loading lookup tables...')
        self.update_idletasks()
        load_file_data()
        self.animate_progress(40, 60)
        self.progress_info.configure(text='Retrieving weather data...')
        self.update_idletasks()
        get_weather()
        self.animate_progress(60, 80)
        self.progress_info.configure(text='Calculating bean dosage...')
        self.update_idletasks()
        bean_data = get_bean_data()
        final_update = 'Done.'
        if weather_error:
            final_update = 'Error: Weather data could not be found'
        self.animate_progress(80, 101)
        image = im.open('beans/' + bean_type + '.png')
        image.thumbnail((300, 300))
        self.image = itk.PhotoImage(image)
        self.display.configure(image=self.image)
        self.progress_info.configure(text=final_update)
        self.bean_info.config(text=bean_data)
        self.update_idletasks()


# run program
BeanApp().mainloop()
