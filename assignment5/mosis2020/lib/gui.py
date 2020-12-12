import tkinter
from tkinter import messagebox
from tkinter import constants
from functools import partial


STATUS_STR = """Energy: {}%
Pay: € {}.00
Factory stock:
    material: {}
    finished product: {}"""

MAX_MSGS = 6 # max number of status messages to show

# Maintains employee and factory state, and generates a multiline status string on each update.
class EmployeeFactoryStatus:
    def __init__(self, tk_parent, status_callback):
        self.tk_parent = tk_parent
        self.status_callback = status_callback
        self.energy = 100
        self.pay = 0
        self.material = 2
        self.finished = 3

    def _refresh(self):
        string = STATUS_STR.format(self.energy, self.pay, self.material, self.finished)
        self.status_callback(string)


    # Employee interface

    def get_energy(self):
        return self.energy

    def increase_energy(self, delta):
        self.energy += delta
        self.energy = min(self.energy, 100)
        self._refresh()
        # Make it realistic :)
        if self.energy <= 0:
            messagebox.showerror(message="You're dead!")
            exit()

    def get_pay(self):
        return self.pay

    def increase_pay(self, delta):
        self.pay += delta
        self._refresh()


    # Factory interface

    def get_material(self):
        return self.material

    def increase_material(self, delta):
        self.material += delta
        self._refresh()

    def get_finished(self):
        return self.finished

    def increase_finished(self, delta):
        self.finished += delta
        self._refresh()


# Multiline stack of status messages (displayed in the middle of the window)
class MessagesStack:
    def __init__(self, widget):
        self.widget = widget
        self.stackptr = 0
        self.lines = [""]*MAX_MSGS

    def push_msg(self):
        self.stackptr += 1

    def pop_msg(self):
        self.lines[self.stackptr] = ""
        self.stackptr -= 1
        self._refresh()

    def set_msg(self, msg):
        self.lines[self.stackptr] = msg
        self._refresh()

    def _refresh(self):
        multiline = '\n'.join(self.lines)
        self.widget['text'] = multiline


def make_buttons(row, comma_separated):
    # remove previous buttons
    for child in row.winfo_children():
        child.destroy()

    if comma_separated != "":
        buttons = [tkinter.Button(row, text=buttontext, pady=10)
            for buttontext in comma_separated.split(',')]
        for b in buttons:
            b.pack(side=constants.LEFT)
        return buttons
    else:
        return []

class GUI:
    def __init__(self, parent, statechart):
        self.statechart = statechart # for raising events when e.g. buttons are clicked

        # UI Layout

        # Highest level: rows, stacked vertically

        toprow = tkinter.Frame(parent)
        toprow.pack(fill=constants.X, padx=4, pady=4)

        msgsrow = tkinter.Frame(parent)
        msgsrow.pack(fill=constants.X, padx=4, pady=4)

        shiftsrow = tkinter.Frame(parent)
        shiftsrow.pack(fill=constants.X, padx=4, pady=4)
        self.shiftsrow = tkinter.Frame(shiftsrow) # inner frame for centering
        self.shiftsrow.pack()

        actionsrow = tkinter.Frame(parent)
        actionsrow.pack(fill=constants.X, padx=4, pady=4)
        self.actionsrow = tkinter.Frame(actionsrow) # inner frame for centering
        self.actionsrow.pack()


        # Top row content

        # Status on the left
        status = tkinter.LabelFrame(toprow, text="Status")
        status.pack(side=constants.LEFT)

        text = tkinter.Label(status, bd=0, justify=constants.LEFT)
        text.pack(fill=constants.X)

        def update_status(str):
            text['text'] = str

        self.employee_factory_status = EmployeeFactoryStatus(parent, update_status)
        self.employee_factory_status._refresh()

        # Go to work / go home - buttons on the right
        workbuttons = tkinter.Frame(toprow)
        workbuttons.pack(side=constants.RIGHT)

        button = tkinter.Button(workbuttons, text="Go to work", command=statechart.employee.raise_go_to_work)
        button.pack(fill=constants.X)

        button = tkinter.Button(workbuttons, text="Go home", command=statechart.employee.raise_go_home)
        button.pack(fill=constants.X)


        # Messages row content

        messages = tkinter.LabelFrame(msgsrow, text="Messages")
        messages.pack(fill=constants.X, side=constants.BOTTOM)

        msgstext = tkinter.Label(messages, bd=0, justify=constants.CENTER)
        msgstext.pack(fill=constants.X)
        
        self.msgs_stack = MessagesStack(msgstext)
        self.msgs_stack.set_msg("Messages appear here")


        # Initial UI state:

        self.shifts_hide()
        self.set_actions("")


    # UI interface

    def push_msg(self):
        self.msgs_stack.push_msg()

    def pop_msg(self):
        self.msgs_stack.pop_msg()

    def set_msg(self, msg):
        self.msgs_stack.set_msg(msg)

    # Hide shift buttons
    def shifts_hide(self):
        self.shift_buttons = make_buttons(self.shiftsrow, "")

    # Show shift buttons
    def shifts_show(self):
        self.shift_buttons = make_buttons(self.shiftsrow, "Unload,Assembly,Load")
        for i, b in enumerate(self.shift_buttons):
            def make_callback(i):
                def cb():
                    self.statechart.employee.raise_shift_clicked(i)
                return cb
            b['command'] = make_callback(i)

    # Mark a shift button with blue background
    def shift_highlight_assigned(self, n):
        for i, b in enumerate(self.shift_buttons):
            if i == n:
                b['bg'] = '#A9C4EB'
                b['activebackground'] = '#A9C4EB'
            else:
                b['bg'] = 'white'
                b['activebackground'] = '#eee'

    # Mark a shift button with green background
    def shift_highlight_active(self, n):
        for i, b in enumerate(self.shift_buttons):
            if i == n:
                b['bg'] = '#B9E0A5'
                b['activebackground'] = '#B9E0A5'
            else:
                b['bg'] = 'white'
                b['activebackground'] = '#eee'

    # Reset all shift buttons' highlight
    def shift_highlight_clear(self):
        for b in self.shift_buttons:
            b['bg'] = 'white'

    def set_actions(self, comma_separated):
        action_buttons = make_buttons(self.actionsrow, comma_separated)
        for b in action_buttons:
            def pressed_callback(text):
                def cb(event):
                    self.statechart.ui.raise_action_pressed(text)
                return cb
            def released_callback(text):
                def cb(event):
                    self.statechart.ui.raise_action_released(text)
                return cb
            b.bind("<Button-1>", pressed_callback(b['text']))
            b.bind("<ButtonRelease-1>", released_callback(b['text']))

