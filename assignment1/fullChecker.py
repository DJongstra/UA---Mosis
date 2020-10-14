import preprocess
# RE: \(CR (\d+)\) AC (\d+)\.\n\(CL \\2\) AB \\1\.\n


from scannerNew import *

__trace__ = False

def makeDot():
    import pydot
    (graph,) = pydot.graph_from_dot_file('./fullFSA.dot')
    graph.write_png('fullFSA.png')


class Automaton(Scanner):

    def __init__(self, stream):

        # superclass constructor
        Scanner.__init__(self, stream)

        # define accepting states set
        self.accepting_states = ["Sfail"]

    def __str__(self):
        return ''

    def transition(self, state, input):
        """
        Encodes transitions and actions
        """

        if state == None:
            # new state
            return "S0"

        elif state == "S0":
            if input == '(':
                # new state
                return "S1"
            else:
                return "Sfail"

        elif state == "S1":
            if input == 'C':
                return "S2"
            else:
                return "Sfail"

        elif state == "S2":
            if input == 'R':
                return "S3_3"
            elif input == 'L':
                return "S7_3"

            else:
                return "Sfail"

        elif state == "S3_3":
            if input == ' ':
                return "S3_4"
            else:
                return "Sfail"

        elif state == "S3_4":
            if input == '0':
                self.m1 = '0'
                return "S3_5"
            elif input == '1':
                self.m1 = '1'
                return "S3_5"
            else:
                return "Sfail"

        elif state == "S3_5":
            if input == ')':
                return "S3_6"
            else:
                return "Sfail"

        elif state == "S3_6":
            if input == ' ':
                return "S3_7"
            else:
                return "Sfail"

        elif state == "S3_7":
            if input == 'A':
                return "S3_8"
            else:
                return "Sfail"

        elif state == "S3_8":
            if input == 'C':
                return "S3_9"
            else:
                return "Sfail"

        elif state == "S3_9":
            if input == ' ':
                return "S3_10"
            else:
                return "Sfail"

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
                return "Sfail"

        elif state == "S3_11":
            if input == '.':
                return "S3_12"
            else:
                return "Sfail"

        elif state == "S3_12":
            if input == '\n':
                return "S3_13"
            else:
                return "Sfail"

        elif state == "S3_13":
            if input == '(':
                return "S3_14"
            else:
                return "Sfail"

        elif state == "S3_14":
            if input == 'C':
                return "S3_15"
            else:
                return "Sfail"

        elif state == "S3_15":
            if input == 'L':
                return "S3_16"
            else:
                return "Sfail"

        elif state == "S3_16":
            if input == ' ':
                return "S3_17"
            else:
                return "Sfail"

        elif state == "S3_17":
            if input == self.m2:
                return "S3_18"
            else:
                return "Sfail"

        elif state == "S3_18":
            if input == ')':
                return "S3_19"
            else:
                return "Sfail"

        elif state == "S3_19":
            if input == ' ':
                return "S3_20"
            else:
                return "Sfail"

        elif state == "S3_20":
            if input == 'A':
                return "S3_21"
            else:
                return "Sfail"

        elif state == "S3_21":
            if input == 'B':
                return "S3_22"
            else:
                return "Sfail"

        elif state == "S3_22":
            if input == ' ':
                return "S3_23"
            else:
                return "Sfail"

        elif state == "S3_23":
            if input == self.m1:
                return "S3_24"
            else:
                return "Sfail"

        elif state == "S3_24":
            if input == '.':
                return "S3_25"
            else:
                return "Sfail"

        elif state == "S3_25":
            if input == '\n':
                return "S0"
            else:
                return "Sfail"

        elif state == "S7_3":
            if input == ' ':
                return "S7_4"
            else:
                return "Sfail"

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
                return "Sfail"

        elif state == "S7_5":
            if input == ')':
                return "S7_6"
            else:
                return "Sfail"

        elif state == "S7_6":
            if input == ' ':
                return "S7_7"
            else:
                return "Sfail"

        elif state == "S7_7":
            if input == 'R':
                return "S7_8"
            else:
                return "Sfail"

        elif state == "S7_8":
            if input == 'M':
                return "S7_9"
            else:
                return "Sfail"

        elif state == "S7_9":
            if input == ' ':
                return "S7_10"
            else:
                return "Sfail"

        elif state == "S7_10":
            nrs = ['0', '1', '2', '3', '4', '5']
            if input in nrs and input != self.m1:
                return "S7_11"
            else:
                return "Sfail"

        elif state == "S7_11":
            if input == ':':
                return "S7_12"
            else:
                return "Sfail"

        elif state == "S7_11":
            if input == ':':
                return "S7_12"
            else:
                return "Sfail"

        elif state == "S7_12":
            chars = string.printable
            if input == '\n':
                return "S0"
            elif input in chars:
                return "S7_12"
            else:
                return "Sfail"

        else:
            return "Sfail"

    def entry(self, state, input):
        pass


if __name__ == '__main__':
    #makeDot()
    str = preprocess.preprocess()
    sc = Automaton(str)
    success = sc.scan()
    if success:
        print(">> recognized failure")
        print(">> aborting")
    else:
        print(">> correct run")
