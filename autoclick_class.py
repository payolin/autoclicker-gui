from pynput import keyboard
from pynput.mouse import Button, Controller
from threading import Thread
import time


class Autoclicker:
    """This is the class used for the Autoclicker program.
    Parameters : - trigger_key (string or key name from pynput, key to press to trigger the autoclick)
                 - sleep_time (int or float, time between clicks)
                 - click_type (pynput button, what button to click with)
    """

    # -1 is on but not clicking, 1 is clicking and 0 is off
    # -1: on, 1: running, 0: off
    state = 0

    def __init__(self, trigger_key, sleep_time, click_type):
        self.trigger_key = trigger_key
        self.sleep_time = sleep_time
        self.click_type = click_type
        self.listener = keyboard.Listener(on_press=self.on_press)

    def click_loop(self):
        mouse = Controller()
        while self.state:
            while self.state == 1:
                if not self.state:  # stop check
                    break
                print("Click")
                mouse.click(self.click_type)
                time.sleep(self.sleep_time)

    def on_press(self, key):
        """Controls state depending on key press"""
        match key:
            case self.trigger_key:
                self.state *= -1  # changes -1 to 1 and 1 to -1
                print(f"state = {self.state}")
            case keyboard.Key.esc:
                self.stop()

    def stop(self):
        self.listener.stop()
        self.state = 0
        print("Exiting program")

    def start(self):
        """Call this function to run the autoclicker"""
        self.state = -1
        self.listener = keyboard.Listener(on_press=self.on_press)
        thr_click_loop = Thread(target=self.click_loop)
        thr_click_loop.start()
        self.listener.start()

    def is_on(self):
        if self.state:
            return True
        else:
            return False


if __name__ == "__main__":
    print("Starting autoclicker")
    auto = Autoclicker(keyboard.Key.f7, 1, Button.left)
    auto.start()
    time.sleep(5)
    auto.stop()
