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

	UserSetpoint = 100.0
	SensorRaw = 99.7
	Ramp = RampController()
	Filter = DeadbandFilter()
	RampEnable = True
	RampReset = False
	RampRateUp = 1.0
	RampRateDown = 2.0
	CurrentValue = 90.0
	Deadband = 0.5
	SmoothSetpoint = None
	SensorFiltered = None
	AtTarget = None
	SensorActive = None

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		self.Ramp(TARGET = self.UserSetpoint, CURRENT = self.CurrentValue, RAMP_UP = self.RampRateUp, RAMP_DOWN = self.RampRateDown, ENABLE = self.RampEnable, RESET = self.RampReset)
		self.SmoothSetpoint = self.Ramp.out
		self.AtTarget = self.Ramp.reached
		self.Filter(IN = self.SensorRaw, DEADBAND = self.Deadband, CENTER = self.SmoothSetpoint)
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
		string += '\nRamp: ' + str(self.Ramp)
		string += '\nFilter: ' + str(self.Filter)
		string += '\nRampEnable: ' + str(self.RampEnable)
		string += '\nRampReset: ' + str(self.RampReset)
		string += '\nRampRateUp: ' + str(self.RampRateUp)
		string += '\nRampRateDown: ' + str(self.RampRateDown)
		string += '\nCurrentValue: ' + str(self.CurrentValue)
		string += '\nDeadband: ' + str(self.Deadband)
		string += '\nSmoothSetpoint: ' + str(self.SmoothSetpoint)
		string += '\nSensorFiltered: ' + str(self.SensorFiltered)
		string += '\nAtTarget: ' + str(self.AtTarget)
		string += '\nSensorActive: ' + str(self.SensorActive)
		log_file.write(string)
		print(string)