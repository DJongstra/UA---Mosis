import subprocess
import json

class LoLARunner:

    def __init__(self):
        self.places = None

    def run_lola(self, filename):

        #change this command as needed
        # place arguments as entries in the list

        cmd = ['lola', '--json=output_queue_overflow_asimstock.json', '--formula="EF AssemblerQ > 10"', filename, '&> AssemblySimStock_Queue_Overflow.log']
        # cmd = ['lola', '--json=output_liveness_asimstock_a.json', '--stubborn=deletion', '--check=full','--formula="AGEF FIREABLE(CubeArrives)"', filename, '&> AssemblySimStock_Liveness_CubeArrives.log']


        # for debugging
        # print("Running cmd: " + str(cmd))

        # run the command
        subprocess.run(" ".join(cmd), shell=True)

        # open the JSON file and check the result
        with open("output_queue_overflow_asimstock.json") as f:
            j = json.load(f)
            result = j['analysis']['result']
            print("Result : " + str(result))

if __name__ == "__main__":

    filename = "AssemblySimStock.lola"

    lr = LoLARunner()
    lr.run_lola(filename)
