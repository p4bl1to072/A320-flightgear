
logprint(LOG_WARN, "Script loaded: Checking if the listener is triggered.");

setlistener("input/arduino/EFIS/CSTR", func(state) {
    logprint(LOG_WARN, "CSTR listener triggered.");
    print("CSTR listener triggered on console.");
    screen.log.write("CSTR listener triggered on screen", 1, 0, 0);
    
    if (state.getBoolValue()) {
        logprint(LOG_WARN, "CSTR state is true.");
        print("CSTR state is true on console.");
        screen.log.write("CSTR state is true on screen", 1, 0, 0);
        
        var propValue = getprop("/input/arduino/EFIS/CSTR");
        logprint(LOG_WARN, "Current CSTR property value: " ~ propValue);
        print("Current CSTR property value: " ~ propValue);
        screen.log.write("Current CSTR property value: " ~ propValue, 1, 0, 0);
        
        if (propValue != 1) {
            logprint(LOG_WARN, "CSTR property value is not 1, activating CSTR.");
            print("CSTR property value is not 1, activating CSTR.");
            screen.log.write("CSTR property value is not 1, activating CSTR.", 1, 0, 0);
            fcu.cpt_efis_btns("cstr");
        } else {
            logprint(LOG_WARN, "CSTR property value is 1, deactivating CSTR.");
            print("CSTR property value is 1, deactivating CSTR.");
            screen.log.write("CSTR property value is 1, deactivating CSTR.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        
        state.setBoolValue(0);
        logprint(LOG_WARN, "CSTR state set to false.");
        print("CSTR state set to false on console.");
        screen.log.write("CSTR state set to false on screen", 1, 0, 0);
    } else {
        logprint(LOG_WARN, "CSTR state is false, no action taken.");
        print("CSTR state is false, no action taken.");
        screen.log.write("CSTR state is false, no action taken.", 1, 0, 0);
    }
}, 1, 0);


logprint(LOG_WARN, "Script loaded: Listener set for /input/arduino/EFIS/CSTR.");



setlistener("input/arduino/EFIS/WPT", func(state)
   {
   if(state.getBoolValue())
      {
      # WPT button
      	if (getprop("/instrumentation/efis/inputs/wpt") != 1) {
		fcu.cpt_efis_btns("wpt");
	} else {
		fcu.cpt_efis_btns("off");
	}
	state.setBoolValue(0);
      }
   else {}
   },1,0);

setlistener("input/arduino/EFIS/VORD", func(state)
   {
   if(state.getBoolValue())
      {
      # VORD button
      	if (getprop("/instrumentation/efis/inputs/VORD") != 1) {
		fcu.cpt_efis_btns("vord");
	} else {
		fcu.cpt_efis_btns("off");
	}
	state.setBoolValue(0);
      }
   else {}
   },1,0);

setlistener("input/arduino/EFIS/NDB", func(state)
   {
   if(state.getBoolValue())
      {
      # NDB button
      	if (getprop("/instrumentation/efis/inputs/NDB") != 1) {
		fcu.cpt_efis_btns("ndb");
	} else {
		fcu.cpt_efis_btns("off");
	}
	state.setBoolValue(0);
      }
   else {}
   },1,0);

setlistener("input/arduino/EFIS/ARPT", func(state)
   {
   if(state.getBoolValue())
      {
      # ARPT button
      	if (getprop("/instrumentation/efis/inputs/arpt") != 1) {
		fcu.cpt_efis_btns("arpt");
	} else {
		fcu.cpt_efis_btns("off");
	}
	state.setBoolValue(0);
      }
   else {}
   },1,0);
