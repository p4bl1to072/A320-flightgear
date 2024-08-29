
# Botones 5
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

var my_setCptND = func() {
    var inputMode = getprop("/input/arduino/EFIS/ND-display-mode");
    screen.log.write("Modo de visualización ND recibido: " ~ inputMode);

    if (inputMode == 1) {
        screen.log.write("Configurando modo ND a ILS");
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("ILS");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(0);
    } else if (inputMode == 2) {
        screen.log.write("Configurando modo ND a VOR");
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("VOR");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(1);
    } else if (inputMode == 3) {
        screen.log.write("Configurando modo ND a NAV");
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("NAV");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(2);
    } else if (inputMode == 4) {
        screen.log.write("Configurando modo ND a ARC");
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("ARC");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(3);
    } else if (inputMode == 5) {
        screen.log.write("Configurando modo ND a PLAN");
        pts.Instrumentation.Efis.Nd.displayMode[0].setValue("PLAN");
        pts.Instrumentation.Efis.Mfd.pnlModeNum[0].setValue(4);
    } else {
        screen.log.write("Modo ND no reconocido: " ~ inputMode);
    }
};

setlistener("/input/arduino/EFIS/ND-display-mode", func() {
    screen.log.write("Listener ND-display-mode activado");
    my_setCptND();
}, 1, 0);

var my_setNDRange = func() {
    var inputRange = getprop("/input/arduino/EFIS/ND-range-nm");
    screen.log.write("Rango de visualización ND recibido: " ~ inputRange);

    var my_rng = 20;
    if (inputRange == 1) {
        screen.log.write("Configurando rango ND a 10");
        my_rng = 10;
    } else if (inputRange == 2) {
        screen.log.write("Configurando rango ND a 20");
        my_rng = 20;
    } else if (inputRange == 3) {
        screen.log.write("Configurando rango ND a 40");
        my_rng = 40;
    } else if (inputRange == 4) {
        screen.log.write("Configurando rango ND a 80");
        my_rng = 80;
    } else if (inputRange == 5) {
        screen.log.write("Configurando rango ND a 160");
        my_rng = 160;
    } else if (inputRange == 6) {
        screen.log.write("Configurando rango ND a 320");
        my_rng = 320;
    } else {
        screen.log.write("Valor de rango ND no reconocido: " ~ inputRange);
        return; # Exit function if input is not recognized
    }

    pts.Instrumentation.Efis.Inputs.rangeNm[0].setValue(my_rng);
}

setlistener("/input/arduino/EFIS/ND-range-nm", func() {
    screen.log.write("Listener ND-range-nm activado");
    my_setNDRange();
}, 1, 0);