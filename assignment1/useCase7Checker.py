from preprocess import preprocess
import string

toCheck = preprocess()

# RE: \(CL ([0-5])\) RM (?!\1)[0-5]\:.*\n

def makeDot():
    import pydot
    (graph,) = pydot.graph_from_dot_file('./useCase7FSA.dot')
    graph.write_png('useCase7FSA.png')


from scannerNew import *

__trace__ = False


class Automaton(Scanner):

    def __init__(self, stream):

        # superclass constructor
        Scanner.__init__(self, stream)

        # define accepting states set
        self.accepting_states = ["S7_13"]

    def __str__(self):
        return ''

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """

        if state == None:
            # new state
            return "S7_0"

        elif state == "S7_0":
            if input == '(':
                # new state
                return "S7_1"
            else:
                return None

        elif state == "S7_1":
            if input == 'C':
                return "S7_2"
            else:
                return None

        elif state == "S7_2":
            if input == 'L':
                return "S7_3"
            else:
                return None

        elif state == "S7_3":
            if input == ' ':
                return "S7_4"
            else:
                return None

        elif state == "S7_4":
            if input == '0':
                self.m1 = '0'
                return "S7_5"
            elif input == '1':
                self.m1 = '1'
                return "S7_5"
            elif input == '2':
                self.m1 = '2'
                return "S7_5"
            elif input == '3':
                self.m1 = '3'
                return "S7_5"
            elif input == '4':
                self.m1 = '4'
                return "S7_5"
            elif input == '5':
                self.m1 = '5'
                return "S7_5"
            else:
                return None

        elif state == "S7_5":
            if input == ')':
                return "S7_6"
            else:
                return None

        elif state == "S7_6":
            if input == ' ':
                return "S7_7"
            else:
                return None

        elif state == "S7_7":
            if input == 'R':
                return "S7_8"
            else:
                return None

        elif state == "S7_8":
            if input == 'M':
                return "S7_9"
            else:
                return None

        elif state == "S7_9":
            if input == ' ':
                return "S7_10"
            else:
                return None

        elif state == "S7_10":
            nrs = ['0', '1', '2', '3', '4', '5']
            if input in nrs and input != self.m1:
                return "S7_11"
            else:
                return None

        elif state == "S7_11":
            if input == ':':
                return "S7_12"
            else:
                return None

        elif state == "S7_11":
            if input == ':':
                return "S7_12"
            else:
                return None


        elif state == "S7_12":
            chars = string.printable
            if input == '\n':
                return "S7_13"
            elif input in chars:
                return "S7_12"
            else:
                return None

        else:
            return None

    def entry(self, state, input):
        pass


if __name__ == '__main__':
    makeDot()