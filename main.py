from pynput import keyboard
from pynput.mouse import Button

from autoclick_class import Autoclicker
from GUI_class import AutoclickGui


def main():
    a = AutoclickGui()
    a.mainloop()


if __name__ == "__main__":
    main()
