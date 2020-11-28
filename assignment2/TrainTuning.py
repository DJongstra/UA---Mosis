from TrainCBD import TrainTuningBlock
from TrainCostModelBlock import StopSimulationException


def tune():
	diff = 1
	Kd = 180
	Ki = 4
	Kp = 565
	for i in range(0,50):
		Kd += i
		Ki += i
		Kp += i
		try:
			print("Trying combination {} : [ Kd = {}, Ki = {}, Kp = {}]".format(i, Kd, Ki, Kp))
			cost = TrainTuningBlock("TrainTuningBlock", Kd=Kd, Ki=Ki, Kp=Kp)
			# Run the simulation
			cost.run(350)
			print(cost.getSignal("OUT_COST"))
		except StopSimulationException:
			print("Not good")
			continue

if __name__ == '__main__':
	tune()