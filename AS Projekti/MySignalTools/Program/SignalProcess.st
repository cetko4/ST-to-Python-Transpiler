
PROGRAM _INIT
	(* Insert code here *)
	 
END_PROGRAM

PROGRAM _CYCLIC
	LimiterFB(IN := AnalogRaw, MIN_LIMIT := -10.0, MAX_LIMIT := 10.0, HYSTERESIS := 0.2);
	LimiterFB();
	
	LimitedSignal := LimiterFB.OUT;
	
	DebounceFB(TRIG := ButtonInput, DEBOUNCE_CYCLES := 20);
	DebounceFB();
	
	IF DebounceFB.VALID_EDGE THEN
		IntegratorEnabled := NOT IntegratorEnabled;
	END_IF;
	
	IntegratorFB(IN := LimitedSignal, DT_STEP := 0.01, ENABLE := IntegratorEnabled, RESET := FALSE, MAX_ACCUM := 100.0, DELTA_LIMIT := 0.5);
	IntegratorFB();
	
	AccumulatedResult := IntegratorFB.OUT;
	
END_PROGRAM

PROGRAM _EXIT
	(* Insert code here *)
	 
END_PROGRAM

