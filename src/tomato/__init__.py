import tkinter as tk
import datetime
import vlc
import os
from collections import namedtuple

Config = namedtuple("Config", ['sound', 'duration', 'update_frequency'])
Config.__new__.__defaults__ = ('bip.mp3', 25, 1000)

class Application(tk.Frame):

    def __init__(self, master = None, config = Config()):
        super().__init__(master)
        self.root = master
        self.root.title('Tomato timer')
        self.root.attributes('-topmost', 'true')
        self.__config = config

        # Vars.
        self.__current = tk.StringVar()
        self.__started = False
        self.__alarm = vlc.MediaPlayer('file://' + self.config.sound)

        # Widgets.
        self.create_widgets()
        self.pack()

        # Reset.
        self.__reset()
        self.do_update()

    def alarm(self):
        self.__alarm.stop()
        self.__alarm.play()

    @property
    def config(self):
        return self.__config

    def do_update(self):
        if self.__started == True:
            self.__update_timer(datetime.timedelta(milliseconds = -self.config.update_frequency))
            # Over.
            if self.__timer == datetime.timedelta():
                self.alarm()
                self.__reset()
        self.root.after(self.config.update_frequency, self.do_update)

    def __update_timer(self, delta, op = '+'):
        if op == '+':
            self.__timer += delta
        elif op == '=':
            self.__timer = delta
        self.__current.set(str(self.__timer))

    def __reset(self):
        self.__started = False
        self.__update_timer(datetime.timedelta(minutes = self.config.duration),
                            op = '=')

    def start(self):
        self.__started = True

    def reset(self):
        self.__alarm.stop()
        self.__reset()

    def create_widgets(self):
        # Timer.
        self.timer_label = tk.Label(self, textvariable = self.__current, font=("Courier", 16))
        self.timer_label.grid(column = 0, row = 0, columnspan = 2)

        # Start button.
        self.start_btn = tk.Button(self)
        self.start_btn["text"] = "START"
        self.start_btn["command"] = self.start
        self.start_btn.grid(column = 0, row = 1)

        # Reset button.
        self.reset_btn = tk.Button(self)
        self.reset_btn["text"] = "RESET"
        self.reset_btn["command"] = self.reset
        self.reset_btn.grid(column = 1, row = 1)
