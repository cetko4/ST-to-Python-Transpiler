############################# TRANSLATED PYTHON CODE ################################

import sys
import time
import datetime
from dataclasses import dataclass, field
from SignalLib import *

class Program:

	_INIT = None
	_EXIT = None


################# DECLARE AND DEFINE USED VARIABLES IN THIS SECTION #################

	AnalogRaw = 12.3
	ButtonInput = False
	AccumulatedResult = None
	LimitedSignal = None
	IntegratorEnabled = None
	LimiterFB = SignalController()
	DebounceFB = Toggler()
	IntegratorFB = Intergrator()

#####################################################################################


	def __init__(self):
		print('_INIT CALLED')
		return

	def _CYCLIC(self):
		#LimiterFB → SignalController.clamp_signal, SignalController.apply_hysteresis
		self.LimiterFB(IN = self.AnalogRaw, MIN_LIMIT = -10.0, MAX_LIMIT = 10.0, HYSTERESIS = 0.2)
		self.LimiterFB
		self.LimitedSignal = self.LimiterFB.OUT
		#DebounceFB → Toggler.detect_edge
		self.DebounceFB(TRIG = self.ButtonInput, DEBOUNCE_CYCLES = 20)
		self.DebounceFB
		if self.DebounceFB.VALID_EDGE:
			self.IntegratorEnabled =  not self.IntegratorEnabled
		#IntegratorFB → Intergrator.accumulate, Intergrator.update_output
		self.IntegratorFB(IN = self.LimitedSignal, DT_STEP = 0.01, ENABLE = self.IntegratorEnabled, RESET = False, MAX_ACCUM = 100.0, DELTA_LIMIT = 0.5)
		self.IntegratorFB
		self.AccumulatedResult = self.IntegratorFB.OUT
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