from pynput import keyboard
from pynput.mouse import Button

from autoclick_class import Autoclicker
from GUI_class import AutoclickGui


def main():
    auto = Autoclicker(keyboard.Key.f7, 1, Button.left)
    a = AutoclickGui(auto)
    a.build()
    a.mainloop()


if __name__ == "__main__":
    main()
