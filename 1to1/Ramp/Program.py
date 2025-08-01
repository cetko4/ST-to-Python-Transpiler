############################# TRANSLATED PYTHON CODE ################################

import sys
import time
import datetime
from dataclasses import dataclass, field
from Ramp_lib import *

class Program:

	_INIT = None
	_EXIT = None


################# DECLARE AND DEFINE USED VARIABLES IN THIS SECTION #################

	UserSetpoint = 25.0
	CurrentValue = 20.0
	RampRateUp = 0.8
	RampRateDown = 1.2
	RampEnable = True
	RampReset = False

	SensorRaw = 24.0
	Deadband = 0.3

	Ramp = RampController()
	Filter = DeadbandFilter()
	SmoothSetpoint = None
	SensorFiltered = None
	AtTarget = None
	SensorActive = None

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		self.Ramp(target = self.UserSetpoint, current = self.CurrentValue, ramp_up = self.RampRateUp, ramp_down = self.RampRateDown, enable = self.RampEnable, reset = self.RampReset)
		self.SmoothSetpoint = self.Ramp.out
		self.AtTarget = self.Ramp.reached
		self.Filter(in_value = self.SensorRaw, deadband = self.Deadband, center = self.SmoothSetpoint)
		self.SensorFiltered = self.Filter.out
		self.SensorActive = self.Filter.is_active
		return

	def __del__(self):
		print('_EXIT CALLED')
		return


	def print_variables(self, log_file):
		string = ''
		string += '\n--------------------------------------\n'
		string += 'log_time:' + str(datetime.datetime.now()) + '\n'
		string += '--------------------------------------'
		string += '\nUserSetpoint: ' + str(self.UserSetpoint)
		string += '\nSensorRaw: ' + str(self.SensorRaw)
		string += '\nRampRateUp: ' + str(self.RampRateUp)
		string += '\nRampRateDown: ' + str(self.RampRateDown)
		string += '\nCurrentValue: ' + str(self.CurrentValue)
		string += '\nDeadband: ' + str(self.Deadband)
		string += '\nSmoothSetpoint: ' + str(self.SmoothSetpoint)
		string += '\nAtTarget: ' + str(self.AtTarget)
		string += '\nSensorActive: ' + str(self.SensorActive)
		string += '\nSensorFiltered: ' + str(self.SensorFiltered)

		string += '\nRampOut: ' + str(self.Ramp.out)
		string += '\nRampPrevOut: ' + str(self.Ramp.prev_out)
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
				
				if cycle_count % 10 == 0:
					program.print_variables(log_file)
					log_file.flush()
				
				cycle_count += 1
				
				time.sleep(0.1)
				
		except KeyboardInterrupt:
			print("\nProgram stopped by user (Ctrl+C)")
			log_file.write("\nProgram stopped by user\n")
		except Exception as e:
			print(f"Error occurred: {e}")
			log_file.write(f"\nError occurred: {e}\n")
		finally:
			log_file.write("Program ended\n")
			print("Program ended")