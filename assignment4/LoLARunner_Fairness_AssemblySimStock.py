import subprocess
import json

class LoLARunner:

    def __init__(self):
        self.places = None

    def run_lola(self, filename):

        #change this command as needed
        # place arguments as entries in the list

        cmd = ['lola', '--json=output_fairness_asimstock.json', '--formula="AG Time_Shape + Time_Assembly + Time_Inspection < 3"', filename, '&> AssemblySimStock_Fairness.log']

        # for debugging
        # print("Running cmd: " + str(cmd))

        # run the command
        subprocess.run(" ".join(cmd), shell=True)

        # open the JSON file and check the result
        with open("output_fairness_asimstock.json") as f:
            j = json.load(f)
            result = j['analysis']['result']
            print("Result : " + str(result))

if __name__ == "__main__":

    filename = "AssemblySimStock.lola"

    lr = LoLARunner()
    lr.run_lola(filename)
