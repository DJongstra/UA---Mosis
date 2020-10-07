import re


def preprocess():
    file = open("./chatProtocolSimulation.trace.txt", "r")
    newFile = open("./processedTrace.txt", "w")
    filetext = file.read()

    re.DOTALL   # to be able to also match newline characters

    filetext = re.sub('##.*\n','', filetext)
    filetext = re.sub('\(CL (\d+)\) RS (\d+)\.\n\(CR \\2\) RR \\1\.\n', '', filetext)     # filter out use case 1
    # use case 2 not filtered out because acceptance is needed in use case 3

    print(filetext)
if __name__ == '__main__':
 preprocess()