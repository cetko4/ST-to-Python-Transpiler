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
	ButtonInput = False
	AccumulatedResult = None
	LimitedSignal = None
	IntegratorEnabled = None
	LimiterFB = SignalLimiter()
	DebounceFB = ToggleDebounce()
	IntegratorFB = SignalIntegrator()

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		self.LimiterFB(IN = self.AnalogRaw, MIN_LIMIT = -10.0, MAX_LIMIT = 10.0, HYSTERESIS = 0.2)
		self.LimiterFB
		self.LimitedSignal = self.LimiterFB.out
		self.DebounceFB(TRIG = self.ButtonInput, DEBOUNCE_CYCLES = 20)
		self.DebounceFB
		if self.DebounceFB.valid_edge:
			self.IntegratorEnabled =  not self.IntegratorEnabled

		self.IntegratorFB(IN = self.LimitedSignal, DT_STEP = 0.01, ENABLE = self.IntegratorEnabled, RESET = False, MAX_ACCUM = 100.0, DELTA_LIMIT = 0.5)
		self.IntegratorFB
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
		string += '\nLimiterFB: ' + str(self.LimiterFB)
		string += '\nDebounceFB: ' + str(self.DebounceFB)
		string += '\nIntegratorFB: ' + str(self.IntegratorFB)
		log_file.write(string)
		print(string)