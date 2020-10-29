#JK
import re
import string
import subprocess, os
from examples.EvenNumberGen.EvenNumberGen import EvenNumberGen
from examples.Fibonacci.Fibonacci import FibonacciGen
from examples.SinGen.SinGen import SinGen

class LaTeXGenerator:

    def __init__(self):
        self.__assignedVariableLetters = []
        self.__blockNameDict = {}
        self.__variableDict = {}
        self.__equationArray = []

    def generateLateX(self, cbd):
        cbdName = cbd.getBlockName()
        print("Generating LaTeX for : " + cbdName)
        print(cbdName)
        blocks = cbd.getBlocks()

        # Flatten the CBD here
        cbd.flatten()

        # For all blocks
        # In the first round, we assign variable letters and create equations for input ports and output ports
        for block in blocks:

            # Add this block to the dictionary of Block Names and Block Name Characters
            blockChar = self.getAssignedBlockCharacter(block.getBlockName())

            inputs = block.getLinksIn()

            # Loop through the inputs
            for inputName in inputs:

                blockInput = inputs[inputName].block
                # Add the block connected to this input to the dictionary of Block Names and Block Name Characters
                blockInputChar = self.getAssignedBlockCharacter(blockInput.getBlockName())

                # Assign a variable for the input link
                self.__variableDict[block.getBlockName() + "." + inputName] = self.generateVariableName(blockChar, inputName)
                # Assign a variable for the output port of the block connected to this input
                self.__variableDict[blockInput.getBlockName() + "." + inputs[inputName].output_port] = self.generateVariableName(blockInputChar, inputs[inputName].output_port)

                # Create an assignment equation that maps the output port to this input port
                self.__equationArray.append(self.constructAssignmentEquation(
                    self.__variableDict[blockInput.getBlockName() + "." + inputs[inputName].output_port],
                    self.__variableDict[block.getBlockName() + "." + inputName]))

        # In the second round, since everything has been assigned a variable letter, we create equations for the block operators
        for block in blocks:
            self.__equationArray.extend(self.constructOperatorEquation(self.__variableDict, block))

        print(self.__variableDict)
        print(self.__equationArray)

        texFileName = cbdName + ".tex"
        pdfFileName = cbdName + ".pdf"

        # We have al the equations, we can now generate the LaTeX
        with open(texFileName, "w") as file:
            file.write("\\documentclass[12pt, letterpaper]{article}\n")
            file.write("\\usepackage[utf8]{inputenc}\n")
            file.write("\\usepackage{amsmath}\n")
            file.write("\\begin{document}\n")
            file.write("Please find below the set of algebraic equations for the flattened " + self.laTeXClean(cbdName) + " CBD:")
            file.write("\\[\n")
            file.write("\\left\\{\n")
            file.write("\\begin{array}{rcl}\n")
            for equation in self.__equationArray:
                file.write(equation + "\\\\")
            file.write("\\end{array}\n")
            file.write("\\right.\n")
            file.write("\\]\n")
            file.write("Given: ")
            file.write("\\begin{itemize}")
            for blockName, variableName in self.__blockNameDict.items():
                file.write("\\item Block \\textbf{" + blockName + "} is represented by variable \\textbf{" + variableName + "}\n")
            file.write("\\end{itemize}")
            file.write("\\end{document}\n")

        # We go further an create the PDF
        x = subprocess.call("pdflatex " + texFileName, shell=True)
        if x != 0:
            print("Exit - code not 0, check result!")
        else:
            os.system("start " + pdfFileName)

        # Communicate completion
        print("Generation of LaTeX for " + cbdName + " complete.")

    """
    Escapes LaTeX special characters in string
    """
    def laTeXClean(self, mystring):
        escapeCharacters = {"#":"\\#", "$":"\\$", "%":"\\%", "&" : "\\&",
                            "~": "\\~{}", "_":"\\_", "^":"\\^{}", "\\":"\\textbackslash",
                            "{":"\\{", "}":"\\}"
        }
        match = re.search("([#$%&~_^\\\{}])",mystring)
        if match != None:
            for group in match.groups():
                mystring = mystring.replace(group, escapeCharacters[group])
        return mystring

    """
    Fetches the variable letter assigned to a block or assigns a new one and returns that.
    """
    def getAssignedBlockCharacter(self, blockName):
        if blockName not in self.__blockNameDict.keys():
            self.__blockNameDict[blockName] = self.assignVariableLetter()
        return self.__blockNameDict[blockName]

    """
    Returns a new character from the alphabet of assignable characters
    """
    def assignVariableLetter(self):
        char = next(char for char in list(string.ascii_lowercase) if char not in self.__assignedVariableLetters)
        self.__assignedVariableLetters.append(char)
        return char

    """
    Generates a variable name for a port based on the Block Name Character
    """
    def generateVariableName(self, blockNameChar, portName):
        portIdentifier = ("_" + re.sub("[^0-9]", "", portName), "_" + portName[1:2])[re.match("[a-zA-Z]*[0-9]+", portName) == None]
        variableString = "var(" + blockNameChar + "." + portName[0] + portIdentifier + ")"
        return variableString

    """
    Constructs assignment equation for the connection from output port to input port
    """
    def constructAssignmentEquation(self, variable, value):
        equationString = variable + " & = & " + value
        return equationString

    """
    Constructs other equations based on where the operator is positioned
    """
    def constructOperatorEquation(self, variableDict, block):
        equationString = ""
        operatorsThatGoInBetween = ["AdderBlock","ProductBlock","ModuloBlock",
                                    "LessThanBlock","EqualsBlock","OrBlock","AndBlock"]
        operatorsThatGoBefore = ["NegatorBlock","NotBlock"]
        blocksWithoutOperations = ["InputPortBlock", "OutputPortBlock", "WireBlock", "TimeBlock",
                                   "LoggingBlock", "SequenceBlock", "DelayBlock"]
        operatorsThatSurround = ["ABSBlock","GenericBlock"]

        blockType = block.getBlockType()

        if (blockType in operatorsThatGoInBetween):
            equationString = self.constructOperatorInBetweenEquation(variableDict, block, blockType)
        elif (blockType in operatorsThatGoBefore):
            equationString = self.constructOperatorGoesBeforeEquation(variableDict, block, blockType)
        elif (blockType in operatorsThatSurround):
            equationString = self.constructOperatorSurroundsEquation(variableDict, block, blockType)
        elif (blockType == "InverterBlock"):
            equationString = self.constructInverterEquation(variableDict, block)
        elif (blockType == "RootBlock"):
            equationString = self.constructRootEquation(variableDict, block)
        elif (blockType == "ConstantBlock"):
            equationString = self.constructConstantAssignmentEquation(variableDict, block)

        return equationString

    """
    Fetches output variables for the output ports of a block
    """
    def getOutputVariables(self, variableDict, block):
        inputs = block.getLinksIn()
        fullInputNames = [block.getBlockName() + "." + inputName for inputName in inputs]
        outputNames = [v for k,v in variableDict.items() if k.startswith(block.getBlockName() + ".") and k not in fullInputNames]
        return outputNames

    """
    Constructs assignment equation for a Constant block
    """
    def constructConstantAssignmentEquation(self, variableDict, block):
        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            equationString = outputVariable + " & = & "
            value = block.getValue()
            equationString += str(value)
            equationStrings.append(equationString)
        return equationStrings

    """
    Constructs operator equation for operators that do in between operands
    """
    def constructOperatorInBetweenEquation(self, variableDict, block, blockType):
        operatorSymbols = {"AdderBlock":"+","ProductBlock":"\\times","ModuloBlock":"\\%",
                                    "LessThanBlock":"<","EqualsBlock":"==","OrBlock":"\\vee","AndBlock":"\\wedge"}
        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            #  the two input ports are equal to the output ports
            equationString = outputVariable + " & = & "
            inputs = block.getLinksIn()
            for index in range(len(inputs)-1):
                inputName = list(inputs)[index]
                inputVariable = variableDict[block.getBlockName() + "." + inputName]
                equationString += inputVariable + " " + operatorSymbols[blockType] + " "
            lastInput = list(inputs)[len(inputs)-1]
            lastInputVariable = variableDict[block.getBlockName() + "." + lastInput]
            equationString += lastInputVariable
            equationStrings.append(equationString)
        return equationStrings

    """
    Constructs operator equation for operators that do before(to the left of in the case of LTR) operands
    """
    def constructOperatorGoesBeforeEquation(self, variableDict, block, blockType):
        operatorSymbols = {"NegatorBlock":"-", "NotBlock":"!"}
        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            equationString = outputVariable + " & = & "
            inputs = block.getLinksIn()
            inputName = list(inputs)[0]
            inputVariable = variableDict[block.getBlockName() + "." + inputName]
            equationString += operatorSymbols[blockType] + inputVariable
            equationStrings.append(equationString)
        return equationStrings

    """
    Constructs operator equation for operators that surround operands
    """
    def constructOperatorSurroundsEquation(self, variableDict, block, blockType):
        blockOperatorMethod = getattr(block, 'getBlockOperator', None)
        blockOperator = ""
        if blockOperatorMethod:
            blockOperator = block.getBlockOperator()
        operatorSymbols = {"ABSBlock": ["\\abs{", "}"],
                           "GenericBlock": [blockOperator+"(",")"]}
        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            equationString = outputVariable + " & = & "
            inputs = block.getLinksIn()
            inputName = list(inputs)[0]
            inputVariable = variableDict[block.getBlockName() + "." + inputName]
            equationString += operatorSymbols[blockType][0] + inputVariable + operatorSymbols[blockType][1]
            equationStrings.append(equationString)
        return equationStrings

    """
    Constructs operator equation for Inverter block
    """
    def constructInverterEquation(self, variableDict, block):
        operatorSymbol = "/"
        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            equationString = outputVariable + " & = & "
            inputs = block.getLinksIn()
            inputName = list(inputs)[0]
            inputVariable = variableDict[block.getBlockName() + "." + inputName]
            equationString += "1" + operatorSymbol + inputVariable
            equationStrings.append(equationString)
        return equationStrings


    """
    Constructs operator equation for Root Block
    """
    def constructRootEquation(self, variableDict, block):
        operatorFirstPart = "\\sqrt[\\leftroot{-2}\\uproot{2}"
        operatorSecondPart = "]{"
        operatorThirdPart = "}"

        inputs = block.getLinksIn()
        firstInputName = list(inputs)[0]
        firstVariable = variableDict[block.getBlockName() + "." + firstInputName]
        secondInputName = list(inputs)[1]
        secondVariable = variableDict[block.getBlockName() + "." + secondInputName]

        equationStrings = []
        for outputVariable in self.getOutputVariables(variableDict, block):
            equationString = outputVariable + " & = & " +operatorFirstPart + secondVariable + operatorSecondPart + firstVariable + operatorThirdPart
            equationStrings.append(equationString)
        return equationStrings

if __name__ == '__main__':

    generator0 = LaTeXGenerator()

    cbdEvenNumberGen = EvenNumberGen("EvenNumberGen")
    # generate the LateX
    generator0.generateLateX(cbdEvenNumberGen)

    generator1 = LaTeXGenerator()
    cbdfibonacci_gen = FibonacciGen("fibonacci_gen")
    # generate the LateX
    generator1.generateLateX(cbdfibonacci_gen)

    generator2 = LaTeXGenerator()
    cbdSinGen = SinGen("SinGen")
    # generate the LateX
    generator2.generateLateX(cbdSinGen)
