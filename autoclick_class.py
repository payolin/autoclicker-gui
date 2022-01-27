from pynput import keyboard
from threading import Thread
import time


class Autoclicker:
    """This is the class used for the Autoclicker program.
    Parameters : -trigger_key (string or key name from pynput; key to press to trigger the autoclick)
                 -sleep_time (int or float, time between clicks)
    """

    # -1 is off, 1 is on, and 0 is for shutting down
    state = -1

    def __init__(self, trigger_key, sleep_time):
        self.trigger_key = trigger_key
        self.sleep_time = sleep_time

    def click_loop(self):
        while self.state:
            while self.state == 1:
                if not self.state:  # stop check
                    break
                print("Click")  # TODO : real click instead of a placeholder
                time.sleep(self.sleep_time)

    def on_press(self, key):
        """Controls state depending on key press"""
        match key:
            case self.trigger_key:
                self.state *= -1  # changes -1 to 1 and 1 to -1
                print(f"state = {self.state}")
            case keyboard.Key.esc:
                print("Exiting autoclicker...")
                self.state = 0
                return False

    def start(self):
        """Call this function to run the autoclicker"""
        thr_click_loop = Thread(target=self.click_loop)
        thr_click_loop.start()
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
            thr_click_loop.join()


if __name__ == "__main__":
    print("Starting autoclicker")
    auto = Autoclicker(keyboard.Key.f7, 5)
    auto.start()
