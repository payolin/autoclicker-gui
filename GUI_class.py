import tkinter as tk
from tkinter.messagebox import showerror
from threading import Thread
from pynput import keyboard
from pynput.mouse import Button

from autoclick_class import Autoclicker


def int_to_click(int_click_type):  # Used to convert the radiobutton variable to a usable click type
    if int_click_type:
        return Button.right
    else:
        return Button.left


class AutoclickGui(tk.Tk):
    """This is a subclass of a tkinter.Tk(). It is used to manage a gui for the autoclick class
    Just make an instance of it to launch the gui, don't forget to mainloop"""
    def __init__(self):
        super().__init__()
        self.title("SimpleAutoclick")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.sleep_time = tk.StringVar(value="1.0")   # |
        self.trigger_key = keyboard.Key.f7            # |  Default values, update is performed on gui launch.
        self.selected_type = tk.IntVar(value=0)       # |  Used as arguments to call the autoclick class

        self.clicker = Autoclicker(
            self.trigger_key,
            float(self.sleep_time.get()),
            int_to_click(self.selected_type),
            0
        )

        # grid building-------------------------------------------------------------------------------------------------
        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # trigger selection---------------------------------------------------------------------------------------------
        def trigger_listener_on_press(key):  # used as a target for a keyboard.Listener
            if key != keyboard.Key.esc:
                self.trigger_key = key

            # enable widgets when a key has been selected
            sleep_time_selector_label["state"] = "normal"
            click_type_selector_label["state"] = "normal"
            trigger_button_label["state"] = "normal"
            start_stop_button["state"] = "normal"
            click_type_selector1["state"] = "normal"
            click_type_selector2["state"] = "normal"
            sleep_time_selector["state"] = "normal"
            click_counter["state"] = "normal"

            trigger_button_label["text"] = f"Current selected key : {self.trigger_key}"
            trigger_button["text"] = "Change autoclick activation key..."
            return False

        def change_trigger_key():  # used as a command for a widget
            change_trigger_key_thread = keyboard.Listener(on_press=trigger_listener_on_press)

            # disable widgets during key selection
            sleep_time_selector_label["state"] = "disabled"
            click_type_selector_label["state"] = "disabled"
            trigger_button_label["state"] = "disabled"
            start_stop_button["state"] = "disabled"
            click_type_selector1["state"] = "disabled"
            click_type_selector2["state"] = "disabled"
            sleep_time_selector["state"] = "disabled"
            click_counter["state"] = "disabled"

            trigger_button["text"] = "Press a key to select it as a trigger..."
            change_trigger_key_thread.start()

        trigger_button_frame = tk.Frame(self)
        trigger_button_frame.grid(row=0, column=0, padx=10, pady=20)

        trigger_button = tk.Button(
            trigger_button_frame,
            width=30,
            text="Change autoclick activation key...",
            command=change_trigger_key
        )

        trigger_button.pack(side="bottom")

        trigger_button_label = tk.Label(trigger_button_frame, text=f"Current selected key: {self.trigger_key}")
        trigger_button_label.pack(side="top")

        # click type selector-------------------------------------------------------------------------------------------
        click_type_selector_frame = tk.Frame(self)
        click_type_selector_frame.grid(row=0, column=1, padx=20)

        radiobutton_frame = tk.Frame(click_type_selector_frame)
        radiobutton_frame.pack(side="bottom")

        click_type_selector1 = tk.Radiobutton(
            radiobutton_frame,
            width=15,
            text="Left Click",
            value=0,
            variable=self.selected_type
        )
        click_type_selector2 = tk.Radiobutton(
            radiobutton_frame,
            width=15,
            text="Right click",
            value=1,
            variable=self.selected_type
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

        sleep_time_selector_label = tk.Label(
            sleep_time_selector_frame, width=30,
            text="Delay between clicks, in seconds:"
        )
        sleep_time_selector_label.pack(side="top")

        # click counter ------------------------------------------------------------------------------------------------
        click_counter = tk.Label(
            self,
            text=f"Total number of clicks : 0"
        )

        click_counter.grid(column=0, row=1, columnspan=3)

        def update_clicker_counter():  # used as a target for the updater thread
            while self.clicker.is_on():
                click_counter["text"] = f"Total number of clicks : {self.clicker.clicks_count}"

        # start & stop button-------------------------------------------------------------------------------------------
        def toggle_on():  # used as a command for a widget, defines what is performed on launch
            try:
                assert float(self.sleep_time.get()) > 0

                # update settings
                self.clicker = Autoclicker(
                    self.trigger_key,
                    float(self.sleep_time.get()),
                    int_to_click(self.selected_type.get()),
                    self.clicker.clicks_count
                )
                clicks_count_thread = Thread(target=update_clicker_counter)  # procedure defined with the widget

                # starting clicking and count updater threads
                self.clicker.start()
                clicks_count_thread.start()

                # disable all the widgets
                sleep_time_selector_label["state"] = "disabled"
                click_type_selector_label["state"] = "disabled"
                trigger_button_label["state"] = "disabled"
                trigger_button["state"] = "disabled"
                click_type_selector1["state"] = "disabled"
                click_type_selector2["state"] = "disabled"
                sleep_time_selector["state"] = "disabled"

                start_stop_button["text"] = f"Autoclicker is running. Press {self.trigger_key} to start clicking."
                start_stop_button["text"] = "Stop autoclicker"
                start_stop_button["command"] = toggle_off
            except (ValueError, AssertionError):
                showerror("Invalid time", "Please select a valid delay time")

        def toggle_off():  # used as a command for a widget
            # re-enable all the widgets
            sleep_time_selector_label["state"] = "normal"
            click_type_selector_label["state"] = "normal"
            trigger_button_label["state"] = "normal"
            trigger_button["state"] = "normal"
            click_type_selector1["state"] = "normal"
            click_type_selector2["state"] = "normal"
            sleep_time_selector["state"] = "normal"

            self.clicker.stop()
            start_stop_button["text"] = "Start autoclicker"
            start_stop_button["command"] = toggle_on

        start_stop_button = tk.Button(
            self,
            text="Start autoclicker",
            command=toggle_on
        )
        start_stop_button.grid(column=0, row=2, columnspan=3, pady=10, sticky="EW")

    def on_closing(self):
        if self.clicker.is_on():
            self.clicker.stop()
        self.destroy()
