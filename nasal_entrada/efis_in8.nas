setlistener("input/arduino/EFIS/CSTR", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/CSTR") != 1) {
            screen.log.write("CSTR activated.", 1, 0, 0);
            fcu.cpt_efis_btns("cstr");
        } else {
            screen.log.write("CSTR deactivated.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/WPT", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/wpt") != 1) {
            screen.log.write("WPT activated.", 1, 0, 0);
            fcu.cpt_efis_btns("wpt");
        } else {
            screen.log.write("WPT deactivated.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/VORD", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/VORD") != 1) {
            screen.log.write("VORD activated.", 1, 0, 0);
            fcu.cpt_efis_btns("vord");
        } else {
            screen.log.write("VORD deactivated.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/NDB", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/NDB") != 1) {
            screen.log.write("NDB activated.", 1, 0, 0);
            fcu.cpt_efis_btns("ndb");
        } else {
            screen.log.write("NDB deactivated.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/ARPT", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/instrumentation/efis/inputs/arpt") != 1) {
            screen.log.write("ARPT activated.", 1, 0, 0);
            fcu.cpt_efis_btns("arpt");
        } else {
            screen.log.write("ARPT deactivated.", 1, 0, 0);
            fcu.cpt_efis_btns("off");
        }
        state.setBoolValue(0);
    }
}, 1, 0);
