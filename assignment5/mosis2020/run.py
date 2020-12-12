import tkinter
from tkinter import constants
from lib.gui import GUI
from lib import timer
from srcgen import statechart
import random

random.seed()

class Util:
    @staticmethod
    def get_random_integer(smallerThan):
        return random.randrange(0, smallerThan)

if __name__ == "__main__":
    tk = tkinter.Tk()

    # Create statechart instance
    sc = statechart.Statechart()
    sc.timer_service = timer.TimerService(tk)

    # Create main window
    gui = GUI(tk, sc)
    tk.resizable(width=constants.NO, height=constants.NO)
    tk.title("Workin' man SIMULATOR")

    # Register callbacks
    sc.util.operation_callback = Util()
    sc.ui.operation_callback = gui
    sc.employee.operation_callback = gui.employee_factory_status
    sc.factory.operation_callback = gui.employee_factory_status

    sc.enter() # Start statechart
    tk.mainloop() # Start UI