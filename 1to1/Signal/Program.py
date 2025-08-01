############################# TRANSLATED PYTHON CODE ################################

import sys
import time
import datetime
from dataclasses import dataclass, field
from SignalProcess_lib import *

class Program:

	_INIT = None
	_EXIT = None


################# DECLARE AND DEFINE USED VARIABLES IN THIS SECTION #################

	AnalogRaw: float = 12.3
	MinLimit: float = -10.0
	MaxLimit: float = 10.0
	hyster: float = 0.2

	deb_cyc: int = 20
	ButtonInput: bool = True
	CycleCounter: int = 0

	AccumulatedResult: float = None
	LimitedSignal: float = None

	IntegratorEnabled: bool = False
	DtStep: float = 0.01
	MaxAccum: float = 100.0
	DeltaLimit: float = 0.5
	ResetFlag: bool = False

	LimiterFB = SignalLimiter()
	DebounceFB = ToggleDebounce()
	IntegratorFB = SignalIntegrator()

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		self.CycleCounter += 1

		if self.CycleCounter == 201:
			self.CycleCounter = 0

		if self.CycleCounter <= 100:
			self.ButtonInput = True
		else:
			if self.CycleCounter >= 101:
				self.ButtonInput = False
		
		self.LimiterFB(in_signal = self.AnalogRaw, min_limit = self.MinLimit, max_limit = self.MaxLimit, hysteresis = self.hyster)
		self.LimitedSignal = self.LimiterFB.out
		
		self.DebounceFB(trig = self.ButtonInput, debounce_cycles = self.deb_cyc)

		self.IntegratorEnabled = self.DebounceFB.valid_edge
		
		self.IntegratorFB(in_signal = self.LimitedSignal, dt_step = self.DtStep, enable = self.IntegratorEnabled, reset = self.ResetFlag, max_accum = self.MaxAccum, delta_limit = self.DeltaLimit)
		self.AccumulatedResult = self.IntegratorFB.out
		return

	def __del__(self):
		print('_EXIT CALLED')
		return


	def print_variables(self, log_file):
		string = ''
		string += '\n--------------------------------------\n'
		string += 'log_time:' + str(datetime.datetime.now()) + '\n'
		string += '--------------------------------------'
		string += '\nAnalogRaw: ' + str(self.AnalogRaw)
		string += '\nButtonInput: ' + str(self.ButtonInput)
		string += '\nAccumulatedResult: ' + str(self.AccumulatedResult)
		string += '\nLimitedSignal: ' + str(self.LimitedSignal)
		string += '\nIntegratorEnabled: ' + str(self.IntegratorEnabled)
		string += '\nDebounce valid_edge: ' + str(self.DebounceFB.valid_edge)
		string += '\nDebounce cycle_counter: ' + str(self.DebounceFB.cycle_counter)
		string += '\nIntegratorFB.enable: ' + str(self.IntegratorFB.enable)
		string += '\nIntegratorFB.accumulated: ' + str(self.IntegratorFB.accumulated)
		log_file.write(string)
		print(string)


if __name__ == "__main__":
	program = Program()
	
	with open("program_log.txt", "w") as log_file:
		log_file.write("Program started\n")
		
		try:
			cycle_count = 0
			
			while True:
				
				program._CYCLIC()
				
				if cycle_count % 1 == 0:
					program.print_variables(log_file)
					log_file.flush()
				
				cycle_count += 1
				
				time.sleep(0.01)
				
		except KeyboardInterrupt:
			print("\nProgram stopped by user (Ctrl+C)")
			log_file.write("\nProgram stopped by user\n")
		except Exception as e:
			print(f"Error occurred: {e}")
			log_file.write(f"\nError occurred: {e}\n")
		finally:
			log_file.write("Program ended\n")
			print("Program ended")