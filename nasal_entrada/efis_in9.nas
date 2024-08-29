

// Botones 5

setlistener("input/arduino/EFIS/CSTR", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/CSTR") != 1) {
            fcu.cpt_efis_btns("cstr");
        } else {
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

 setlistener("input/arduino/EFIS/WPT", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/wpt") != 1) {
            fcu.cpt_efis_btns("wpt");
        } else {
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/VORD", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/VORD") != 1) {
            fcu.cpt_efis_btns("vord");
        } else {
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/NDB", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/NDB") != 1) {
            fcu.cpt_efis_btns("ndb");
        } else {
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/ARPT", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/arpt") != 1) {
            fcu.cpt_efis_btns("arpt");
        } else {
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

// Selectores 8pos

// Define the function to set the display mode based on the input value
//Inputs are [1,6] and modes are [0,4]. Input may need to be limited to 5 to work properly
var my_setCptND = func() {
    var inputMode = getprop("/input/arduino/EFIS/ND-display-mode");
    
    if (inputMode == 1) {
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("ILS");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(0);
    } else if (inputMode == 2) {
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("VOR");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(1);
    } else if (inputMode == 3) {
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("NAV");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(2);
    } else if (inputMode == 4) {
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("ARC");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(3);
    } else if (inputMode == 5) {
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("PLAN");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(4);
    }
}

// Add a listener to watch for changes to the input property
setlistener("/input/arduino/EFIS/ND-display-mode", func() {
    my_setCptND();
}, 1, 0);

var my_setNDRange = func() {
    var inputValue = getprop("/input/arduino/EFIS/ND-range-nm");

    // Map input values to the corresponding range
    var rng;
    if (inputValue <= 10) {
        rng = 10;
    } else if (inputValue <= 20) {
        rng = 20;
    } else if (inputValue <= 30) {
        rng = 40;
    } else if (inputValue <= 40) {
        rng = 80;
    } else if (inputValue <= 50) {
        rng = 160;
    } else {
        rng = 320;
    }

    pts.Instrumentation.Efis.Inputs.rangeNm[0].setValue(rng);
}

setlistener("/input/arduino/EFIS/ND-range-nm", func() {
    my_setNDRange();
}, 1, 0);

