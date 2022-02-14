import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

from autoclick_class import Autoclicker


class AutoclickGui:
    root = tk.Tk()

    def __init__(self, clicker: Autoclicker):
        self.clicker = clicker

    def mainloop(self):
        self.root.tk.mainloop()

    def build(self):
        # grid building-------------------------------------------------------------------------------------------------
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

        # trigger selection button and label----------------------------------------------------------------------------
        trigger_button_frame = ttk.Frame(self.root)
        trigger_button_frame.grid(row=0, column=0, padx=10, pady=20)

        trigger_button = ttk.Button(
            trigger_button_frame,
            text="Change autoclick activation key..."
        )
        trigger_button.pack(side="bottom")

        trigger_button_label = ttk.Label(trigger_button_frame, text="Current selected key:")
        trigger_button_label.pack(side="top")

        # click type selector-------------------------------------------------------------------------------------------
        click_type_selector_frame = ttk.Frame(self.root)
        click_type_selector_frame.grid(row=0, column=1, padx=20)

        radiobutton_frame = ttk.Frame(click_type_selector_frame)
        radiobutton_frame.pack(side="bottom")

        selected_type = tk.IntVar()
        click_type_selector1 = ttk.Radiobutton(
            radiobutton_frame,
            text="Left Click",
            value=0,
            variable=selected_type
        )
        click_type_selector2 = ttk.Radiobutton(
            radiobutton_frame,
            text="Right click",
            value=1,
            variable=selected_type
        )
        click_type_selector1.pack(side="top")
        click_type_selector2.pack(side="bottom")

        click_type_selector_label = ttk.Label(click_type_selector_frame, text="Selected click :")
        click_type_selector_label.pack(side="top")

        # sleep time selector-------------------------------------------------------------------------------------------
        sleep_time_selector_frame = ttk.Frame(self.root)
        sleep_time_selector_frame.grid(row=0, column=2, padx=10, pady=20)

        selected_sleep_time = tk.StringVar()
        sleep_time_selector = ttk.Entry(
            sleep_time_selector_frame,
            textvariable=selected_sleep_time
        )
        sleep_time_selector.pack(side="bottom")

        sleep_time_selector_label = ttk.Label(sleep_time_selector_frame, text="Delay between clicks, in seconds:")
        sleep_time_selector_label.pack(side="top")

        # start & stop button-------------------------------------------------------------------------------------------
        def stop_checker():
            while self.clicker.is_on():
                time.sleep(0.1)
            if start_stop_button["text"] != "Start autoclicker":
                start_stop_button["text"] = "Start autoclicker"
                start_stop_button["command"] = toggle_on

        def toggle_on():
            start_stop_button["text"] = "Clicker is on. Press f7 and the program will toggle autoclicking"
            time.sleep(0.1)
            self.clicker.start()
            time.sleep(2)
            start_stop_button["text"] = "Turn clicker off"
            start_stop_button["command"] = toggle_off
            stop_checker_thread = Thread(target=stop_checker)
            stop_checker_thread.start()

        def toggle_off():
            self.clicker.stop()
            start_stop_button["text"] = "Start autoclicker"
            start_stop_button["command"] = toggle_on

        start_stop_button = ttk.Button(
            self.root,
            text="Start autoclicker",
            command=toggle_on
        )

        start_stop_button.grid(column=0, row=1, columnspan=3, pady=10, sticky="EW")
