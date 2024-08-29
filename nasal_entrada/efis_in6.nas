
setlistener("input/arduino/EFIS/CSTR", func(state)
   {
   if(state.getBoolValue())
      {
      # CSTR button
      	if (getprop("/input/arduino/EFIS/CSTR") != 1) {
		fcu.cpt_efis_btns("cstr");
	} else {
		fcu.cpt_efis_btns("off");
	}
	state.setBoolValue(0);
      }
   else {}
   },1,0);

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
