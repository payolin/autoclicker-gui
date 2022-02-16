import time
import tkinter as tk
from tkinter.messagebox import showerror
from threading import Thread
from pynput import keyboard
from pynput.mouse import Button, Controller

import autoclick_class
from autoclick_class import Autoclicker


class AutoclickGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("SimpleAutoclick")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.sleep_time = tk.StringVar(value="1")
        self.default_trigger_key = keyboard.Key.f7
        self.default_click_type = Button.left

        self.clicker = autoclick_class.Autoclicker(
            self.default_trigger_key,
            float(self.sleep_time.get()),
            self.default_click_type
        )

        # grid building-------------------------------------------------------------------------------------------------
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # trigger selection----------------------------------------------------------------------------
        trigger_button_frame = tk.Frame(self)
        trigger_button_frame.grid(row=0, column=0, padx=10, pady=20)

        trigger_button = tk.Button(
            trigger_button_frame,
            text="Change autoclick activation key..."
        )
        trigger_button.pack(side="bottom")

        trigger_button_label = tk.Label(trigger_button_frame, text="Current selected key:")
        trigger_button_label.pack(side="top")

        # click type selector-------------------------------------------------------------------------------------------
        click_type_selector_frame = tk.Frame(self)
        click_type_selector_frame.grid(row=0, column=1, padx=20)

        radiobutton_frame = tk.Frame(click_type_selector_frame)
        radiobutton_frame.pack(side="bottom")

        selected_type = tk.IntVar()
        click_type_selector1 = tk.Radiobutton(
            radiobutton_frame,
            text="Left Click",
            value=0,
            variable=selected_type
        )
        click_type_selector2 = tk.Radiobutton(
            radiobutton_frame,
            text="Right click",
            value=1,
            variable=selected_type
        )
        click_type_selector1.pack(side="top")
        click_type_selector2.pack(side="bottom")

        click_type_selector_label = tk.Label(click_type_selector_frame, text="Selected click :")
        click_type_selector_label.pack(side="top")

        # sleep time selector-------------------------------------------------------------------------------------------
        sleep_time_selector_frame = tk.Frame(self)
        sleep_time_selector_frame.grid(row=0, column=2, padx=10, pady=20)

        sleep_time_selector = tk.Entry(
            sleep_time_selector_frame,
            textvariable=self.sleep_time
        )
        sleep_time_selector.pack(side="bottom")

        sleep_time_selector_label = tk.Label(sleep_time_selector_frame, text="Delay between clicks, in seconds:")
        sleep_time_selector_label.pack(side="top")

        # start & stop button-------------------------------------------------------------------------------------------
        def stop_checker():
            while self.clicker.is_on():
                time.sleep(0.1)
            if start_stop_button["text"] != "Start autoclicker":
                start_stop_button["text"] = "Start autoclicker"
                start_stop_button["command"] = toggle_on

        def toggle_on():
            try:
                assert float(self.sleep_time.get()) > 0
                print(self.sleep_time.get())

                self.clicker = autoclick_class.Autoclicker(
                    self.default_trigger_key,
                    float(self.sleep_time.get()),
                    self.default_click_type
                )
                start_stop_button["text"] = "Clicker is on. Press f7 and the program will toggle auto-clicking"
                print("t")
                time.sleep(2)
                self.clicker.start()
                start_stop_button["text"] = ""
                time.sleep(2)
                start_stop_button["text"] = "Turn clicker off"
                start_stop_button["command"] = toggle_off
                stop_checker_thread = Thread(target=stop_checker)
                stop_checker_thread.start()

            except (ValueError, AssertionError):
                showerror("Invalid time", "Please select a valid delay time")

        def toggle_off():
            self.clicker.stop()
            start_stop_button["text"] = "Start autoclicker"
            start_stop_button["command"] = toggle_on

        start_stop_button = tk.Button(
            self,
            text="Start autoclicker",
            command=toggle_on
        )
        start_stop_button.grid(column=0, row=1, columnspan=3, pady=10, sticky="EW")

    def on_closing(self):
        if self.clicker.is_on():
            self.clicker.stop()
        self.destroy()






