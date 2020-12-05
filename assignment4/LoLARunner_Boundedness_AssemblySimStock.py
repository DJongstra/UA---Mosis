import subprocess
import json

class LoLARunner:

    def __init__(self):
        self.places = None

    # load the place names
    def load_places(self, places):
        places = places.replace(";", "").split(",")
        self.places = [p.strip() for p in places]

    def run_lola(self, filename):

        # loop through each place
        for p in self.places:

            #change this command as needed
            # place arguments as entries in the list

            cmd = ['lola', '--quiet', '--json=output_boundedness_asimstock.json', '--search=cover', '--encoder=full', '--formula="AG ' + p +' < oo"', '--markinglimit=1000', filename]

            # for debugging
            # print("Running cmd: " + str(cmd))

            # run the command
            subprocess.run(" ".join(cmd), shell=True)

            # open the JSON file and check the result
            with open("output_boundedness_asimstock.json") as f:
                j = json.load(f)
                result = j['analysis']['result']
                print("Result for " + p + ": " + str(result))

if __name__ == "__main__":

    # CHANGE THESE VARIABLES FOR YOUR SOLUTION
    # YOU CAN COPY THE PLACE NAMES FROM THE LOLA FILE
    places = """AcceptedAmount,
	AmountOfTimeSteps,
	AssemAble,
	AssemblerQ,
	AssemblyActive,
	AssemblyAvailable,
	AssemUnable,
	CubesInQ,
	CubeStock,
	CylindersInQ,
	CylinderStock,
	InspAble,
	Inspected,
	InspectinAvailable,
	Inspecting,
	InspQ,
	InspQAvailable,
	InspUnable,
	RemakeAmount,
	RemakeNotQueued,
	RemakeQ,
	ThrashedAmount,
	Time_Assembly,
	Time_AssemblyExecuted,
	Time_InspectingExecuted,
	Time_Inspection,
	Time_NextAvailable,
	Time_Shape,
	Time_ShapeExecuted,
	TimeInAssembly,
	TimeInInsp,
	TotalInQAssem;"""
    filename = "AssemblySimStock.lola"

    lr = LoLARunner()
    lr.load_places(places)
    lr.run_lola(filename)
