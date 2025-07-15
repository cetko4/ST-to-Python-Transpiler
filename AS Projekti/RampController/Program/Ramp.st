
PROGRAM _INIT
	(* Insert code here *)
	 
END_PROGRAM

PROGRAM _CYCLIC
	(** --- RAMP CONTROLLER LOGIC --- **)
	Ramp(TARGET := UserSetpoint, CURRENT := CurrentValue, RAMP_UP := RampRateUp, RAMP_DOWN := RampRateDown, ENABLE := RampEnable, RESET := RampReset);
	SmoothSetpoint := Ramp.OUT;
	AtTarget := Ramp.REACHED;
   
	(** --- DEADBAND FILTER LOGIC --- **)
	Filter(IN := SensorRaw, DEADBAND := Deadband, CENTER := SmoothSetpoint);
	SensorFiltered := Filter.OUT;
	SensorActive := Filter.IS_ACTIVE;
	 
END_PROGRAM

PROGRAM _EXIT
	(* Insert code here *)
	 
END_PROGRAM

