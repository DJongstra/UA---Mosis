import re

def preprocess():
    file = open("./chatProtocolSimulation.trace.txt", "r")
    # file = open("./chatProtocolSimulationFixed.trace.txt", "r")
    filetext = file.read()

    re.DOTALL   # to be able to also match newline characters

    filetext = re.sub('##.*\n','', filetext)    # filtering out all the comments
    filetext = re.sub('\(CL (\d+)\) RS (\d+)\.\n\(CR \\2\) RR \\1\.\n', '', filetext)     # filter out use case 1
    # use case 2 not filtered out because acceptance line is needed in use case 3
    filetext = re.sub('\(CR (\d+)\) RC (\d+)\.\n\(CL \\2\) RB \\1\.\n', '', filetext)     # filter out use case 4
    filetext = re.sub('\(CL (\d+)\) SY: .*\n\(CR (\d+)\) RM \\1:.*\n\(CR \\2\) SM \\1:.*\n', '', filetext)  # filter out use case 5 + 6

    return filetext


if __name__ == '__main__':
 print(preprocess())