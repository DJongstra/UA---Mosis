import subprocess
import json

class LoLARunner:

    def __init__(self):
        self.places = None

    def run_lola(self, filename):

        #change this command as needed
        # place arguments as entries in the list

        cmd = ['lola', '--json=output_liveness_asimstock.json', '--formula="AGEF FIREABLE(Assembly)"', '--markinglimit=602207402', filename, '&> AssemblySimStock_Liveness.log']
        # cmd = ['lola', '--json=output_liveness_asimstock_a.json', '--stubborn=deletion', '--check=full','--formula="AGEF FIREABLE(CubeArrives)"', filename, '&> AssemblySimStock_Liveness_CubeArrives.log']


        # for debugging
        # print("Running cmd: " + str(cmd))

        # run the command
        subprocess.run(" ".join(cmd), shell=True)

        # open the JSON file and check the result
        with open("output_liveness_asimstock.json") as f:
            j = json.load(f)
            result = j['analysis']['result']
            print("Result : " + str(result))

if __name__ == "__main__":

    filename = "AssemblySimStock.lola"

    lr = LoLARunner()
    lr.run_lola(filename)
