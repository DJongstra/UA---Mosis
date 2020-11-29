from TrainCBD import TrainTuningBlock
from TrainCostModelBlock import StopSimulationException


def tune():
	costs = []
	combinations = {}
	for d in range(0,15):
		for i in range(0,6):
			for p in range(0, 15):
				Kd = 180 + d
				Ki = 4 + i
				Kp = 565 + p
				try:
					key = "[ Kd = {}, Ki = {}, Kp = {} ]".format(Kd, Ki, Kp)
					print("Trying combination {} : [ Kd = {}, Ki = {}, Kp = {} ]".format(d, Kd, Ki, Kp))
					cost = TrainTuningBlock("TrainTuningBlock", Kd=Kd, Ki=Ki, Kp=Kp)
					# Run the simulation
					cost.run(3500)
					cummulativeCost = cost.getSignal("OUT_COST")[-1].value
					costs.append(cummulativeCost)
					combinations[key] = cummulativeCost
					# print(cummulativeCost)
					print("Successful combination {} : [ Kd = {}, Ki = {}, Kp = {} ] COST : {}".format(i, Kd, Ki, Kp, cummulativeCost))
				except StopSimulationException:
					print("Not good")
					continue
	print(combinations)
	print(costs)
	minimum_cost = min(costs)
	print(minimum_cost)
	for combination, cost in combinations.items():
		if cost == minimum_cost:
			print("Best combination with cost {} :: {} ".format(cost, combination))

if __name__ == '__main__':
	tune()