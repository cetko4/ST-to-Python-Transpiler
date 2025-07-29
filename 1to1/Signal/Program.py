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

	AnalogRaw = 12.3
	ButtonInput = True
	AccumulatedResult = None
	LimitedSignal = None
	IntegratorEnabled = False
	LimiterFB = SignalLimiter()
	DebounceFB = ToggleDebounce()
	IntegratorFB = SignalIntegrator()

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		self.LimiterFB(in_signal = self.AnalogRaw, min_limit = -10.0, max_limit = 10.0, hysteresis = 0.2)
		self.LimitedSignal = self.LimiterFB.out
		
		self.DebounceFB(trig = self.ButtonInput, debounce_cycles = 20)
		if self.DebounceFB.valid_edge:
			self.IntegratorEnabled = not self.IntegratorEnabled
		
		self.IntegratorFB(in_signal = self.LimitedSignal, dt_step = 0.01, enable = self.IntegratorEnabled, reset = False, max_accum = 100.0, delta_limit = 0.5)
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
			button_toggle_interval = 200
			button_press_duration = 50
			
			while True:
				cycle_in_period = cycle_count % button_toggle_interval
				current_button_state = cycle_in_period < button_press_duration
				
				program.ButtonInput = current_button_state
				
				program._CYCLIC()
				
				if cycle_count % 50 == 0:
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