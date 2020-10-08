from preprocess import preprocess

toCheck = preprocess()

# RE: \(CR (\d+)\) AC (\d+)\.\n\(CL \\2\) AB \\1\.\n

def makeDot():
    import pydot
    (graph,) = pydot.graph_from_dot_file('./useCase3FSA.dot')
    graph.write_png('useCase3FSA.png')


from scannerNew import *

__trace__ = False


class Automaton(Scanner):

    def __init__(self, stream):

        # superclass constructor
        Scanner.__init__(self, stream)

        # define accepting states set
        self.accepting_states = ["S3_26"]

    def __str__(self):
        return ''

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """

        if state == None:
            # new state
            return "S3_0"

        elif state == "S3_0":
            if input == '(':
                # new state
                return "S3_1"
            else:
                return None

        elif state == "S3_1":
            if input == 'C':
                return "S3_2"
            else:
                return None

        elif state == "S3_2":
            if input == 'R':
                return "S3_3"
            else:
                return None

        elif state == "S3_3":
            if input == ' ':
                return "S3_4"
            else:
                return None

        elif state == "S3_4":
            if input == '0':
                self.m1 = '0'
                return "S3_5"
            elif input == '1':
                self.m1 = '1'
                return "S3_5"
            else:
                return None

        elif state == "S3_5":
            if input == ')':
                return "S3_6"
            else:
                return None

        elif state == "S3_6":
            if input == ' ':
                return "S3_7"
            else:
                return None

        elif state == "S3_7":
            if input == 'A':
                return "S3_8"
            else:
                return None

        elif state == "S3_8":
            if input == 'C':
                return "S3_9"
            else:
                return None

        elif state == "S3_9":
            if input == ' ':
                return "S3_10"
            else:
                return None

        elif state == "S3_10":
            if input == '0':
                self.m2 = '0'
                return "S3_11"
            elif input == '1':
                self.m2 = '1'
                return "S3_11"
            elif input == '2':
                self.m2 = '2'
                return "S3_11"
            elif input == '3':
                self.m2 = '3'
                return "S3_11"
            elif input == '4':
                self.m2 = '4'
                return "S3_11"
            elif input == '5':
                self.m2 = '5'
                return "S3_11"
            else:
                return None

        elif state == "S3_11":
            if input == '.':
                return "S3_12"
            else:
                return None

        elif state == "S3_12":
            if input == '\n':
                return "S3_13"
            else:
                return None

        elif state == "S3_13":
            if input == '(':
                return "S3_14"
            else:
                return None

        elif state == "S3_14":
            if input == 'C':
                return "S3_15"
            else:
                return None

        elif state == "S3_15":
            if input == 'L':
                return "S3_16"
            else:
                return None

        elif state == "S3_16":
            if input == ' ':
                return "S3_17"
            else:
                return None

        elif state == "S3_17":
            if input == self.m2:
                return "S3_18"
            else:
                return None

        elif state == "S3_18":
            if input == ')':
                return "S3_19"
            else:
                return None

        elif state == "S3_19":
            if input == ' ':
                return "S3_20"
            else:
                return None

        elif state == "S3_20":
            if input == 'A':
                return "S3_21"
            else:
                return None

        elif state == "S3_21":
            if input == 'B':
                return "S3_22"
            else:
                return None

        elif state == "S3_22":
            if input == ' ':
                return "S3_23"
            else:
                return None

        elif state == "S3_23":
            if input == self.m1:
                return "S3_24"
            else:
                return None

        elif state == "S3_24":
            if input == '.':
                return "S3_25"
            else:
                return None

        elif state == "S3_25":
            if input == '\n':
                return "S3_26"
            else:
                return None

        else:
            return None

    def entry(self, state, input):

        if state == "S2":
            self.value = 2 * self.value
        elif state == "S3":
            self.value = 2 * self.value + 1


if __name__ == '__main__':
    makeDot()