import subprocess
import json

class LoLARunner:

    def __init__(self):
        self.places = None

    def run_lola(self, filename):

        #change this command as needed
        # place arguments as entries in the list

        # cmd = ['lola', '--quiet', '--json=output_deadlock_asimstock.json', '--formula="EF DEADLOCK"', '--search=sweep', filename]
        # cmd = ['lola', '--quiet', '--json=output_deadlock_asimstock.json', '--formula="EF DEADLOCK"', '--search=sweep', '--markinglimit=1000000', filename]
        # cmd = ['lola', '--json=output_deadlock_asimstock.json', '--formula="EF DEADLOCK"', '--search=sweep', '--cycle', '--markinglimit=10013607',filename]
        cmd = ['lola', '--json=output_deadlock_asimstock.json', '--formula="EF DEADLOCK"', '--search=cover', '--cycle',filename]


        # for debugging
        # print("Running cmd: " + str(cmd))

        # run the command
        subprocess.run(" ".join(cmd), shell=True)

        # open the JSON file and check the result
        with open("output_deadlock_asimstock.json") as f:
            j = json.load(f)
            result = j['analysis']['result']
            print("Result : " + str(result))

if __name__ == "__main__":

    filename = "AssemblySimStock.lola"

    lr = LoLARunner()
    lr.run_lola(filename)
