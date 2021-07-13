import tkinter
import os
import pyglet
from time import sleep
from datetime import datetime
from requests import get as get_request


def relPath(suffix_path):
    final_path = os.path.dirname(__file__) + '\\' + suffix_path
    return final_path


pyglet.font.add_file(relPath('requirements\\Nunito-Regular.ttf'))
pyglet.font.add_file(relPath('requirements\\Roboto-Medium.ttf'))
pyglet.font.add_file(relPath('requirements\\Roboto-Light.ttf'))
pyglet.font.add_file(relPath('requirements\\Ubuntu-Regular.ttf'))


class AppInterface(tkinter.Tk):
    bg_color = '#262624'
    fg_color = '#ffffff'
    menu_btn_active = False

    def __init__(self):
        super().__init__()
        x_slice = (self.winfo_screenwidth() / 2) - 640
        y_slice = (self.winfo_screenheight() / 2) - 360
        self.geometry('%dx%d+%d+%d' % (1280, 720, x_slice, y_slice))
        self.minsize(640, 360)
        self.maxsize(1920, 1080)
        self.title("Splash Clock")
        self.iconbitmap(relPath('media\\icon.ico'))
        self.config(bg=self.bg_color)
        self.header_text = tkinter.StringVar()
        header = tkinter.Label(textvariable=self.header_text,
                               bg=self.bg_color,
                               fg=self.fg_color,
                               font=('Nunito', 40),
                               anchor='n')
        header.pack(side=tkinter.TOP, pady=(25, 0))
        self.clockScreen()
        self.blankSpace(self), self.blankSpace(self), self.blankSpace(self)
        self.blankSpace(self), self.menuButton(self, "Clock", padx=54), self.blankSpace(self)
        self.blankSpace(self), self.menuButton(self, "Alarm"), self.blankSpace(self)
        self.blankSpace(self), self.menuButton(self, "Timer", padx=53), self.blankSpace(self)
        self.blankSpace(self), self.menuButton(self, "Stopwatch", target=self.stopwatchScreen, padx=20)

    @classmethod
    def blankSpace(cls, container):
        tkinter.Label(container, bg=cls.bg_color).pack()

    def setButtonActivity(self):
        if self.menu_btn_active:
            self.menu_btn_active = False
        else:
            self.menu_btn_active = True

    def _buttonCommand(self, action):
        self.setButtonActivity()
        action()

    def menuButton(self, container, text, padx=50, target=print):
        menu_btn = tkinter.Button(container,
                                  activebackground='#22a6b3',
                                  text=text,
                                  command=target,
                                  bg=self.fg_color,
                                  fg=self.bg_color,
                                  borderwidth=0,
                                  font=('Nunito', 20, 'bold'),
                                  padx=padx,
                                  pady=None)
        menu_btn.bind('<Enter>', lambda _: menu_btn.config(bg='#7bed9f'))
        menu_btn.bind('<Leave>', lambda _: menu_btn.config(bg=self.fg_color))
        menu_btn.pack(padx=(0, 150))

    def clockScreen(self):
        self.header_text.set("Splash Clock | Clock")
        time_str, date_str, weather_str = tkinter.StringVar(), tkinter.StringVar(), tkinter.StringVar()

        def liveTime():
            time_str.set(datetime.now().strftime('%I : %M : %S %p'))
            date_str.set(datetime.now().strftime('%A, %dth of %B %Y'))
            clock_widget.after(950, liveTime)

        def liveWeather():
            _deg_celsius_sign = u'\N{DEGREE SIGN}' + 'C'
            api_key = 'ffc8cf657d7bb60f9b2797459feb6d1f'
            city_name = 'Bilaspur'
            fetch_url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city_name}'
            weather_data = get_request(fetch_url).json()
            weather_output = f"""{'{:.2f}'.format(weather_data['main']['temp'] - 273.15)} {_deg_celsius_sign}
{weather_data['weather'][0]['description'].title()}"""
            weather_str.set(weather_output)
            weather_widget.after(3600000, liveWeather)

        dt_frame = tkinter.Frame(self, bg=self.bg_color, borderwidth=0, padx=100)
        clock_widget = tkinter.Label(dt_frame, textvariable=time_str,
                                     bg=self.bg_color,
                                     fg=self.fg_color,
                                     font=('Roboto Medium', 48, 'bold'),
                                     anchor='center')
        date_widget = tkinter.Label(dt_frame, textvariable=date_str,
                                    bg=self.bg_color,
                                    fg=self.fg_color,
                                    font=('Roboto Light', 20,),
                                    anchor='center')
        weather_widget = tkinter.Label(dt_frame, textvariable=weather_str,
                                       bg=self.bg_color,
                                       fg='#a29bfe',
                                       font=('Ubuntu', 20, 'bold'),
                                       anchor='center')
        clock_widget.pack(), date_widget.pack(), self.blankSpace(dt_frame), weather_widget.pack()
        self.blankSpace(dt_frame), self.blankSpace(dt_frame), self.blankSpace(dt_frame), self.blankSpace(dt_frame)
        self.blankSpace(dt_frame)
        dt_frame.pack(side=tkinter.RIGHT)
        liveTime()
        liveWeather()

    def alarmScreen(self):
        pass

    def stopwatchScreen(self):
        self.header_text.set("Splash Clock | Stopwatch")
        stopwatch_frame = tkinter.Frame(self, bg=self.bg_color, borderwidth=0, padx=100)
        counter, counter_slack = 0, tkinter.IntVar()
        stopwatch_widget = tkinter.Label(stopwatch_frame, textvariable=counter_slack,
                                         bg=self.bg_color,
                                         fg=self.fg_color,
                                         font=('Roboto Medium', 48, 'bold'),
                                         anchor='center')
        stopwatch_widget.pack()
        stopwatch_frame.pack(side=tkinter.RIGHT)


UI = AppInterface()
UI.mainloop()
