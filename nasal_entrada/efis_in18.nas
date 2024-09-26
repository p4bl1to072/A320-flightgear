
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


# Function to toggle STD based on external control
var toggleSTDControl = func(state) {
    var shouldBeSTD = getprop("/input/arduino/EFIS/PULL_STD");
    var currentSTD = pts.Instrumentation.Altimeter.std.getBoolValue();

    if (shouldBeSTD == 1 and currentSTD == 0) {
        # Activate STD mode if it isn't already active
        pts.Instrumentation.Altimeter.oldQnh.setValue(pts.Instrumentation.Altimeter.settingInhg.getValue());
        pts.Instrumentation.Altimeter.settingInhg.setValue(29.92);
        pts.Instrumentation.Altimeter.std.setBoolValue(1);
    } else if (shouldBeSTD == 0 and currentSTD == 1) {
        # Deactivate STD mode if it is currently active
        pts.Instrumentation.Altimeter.settingInhg.setValue(pts.Instrumentation.Altimeter.oldQnh.getValue());
        pts.Instrumentation.Altimeter.std.setBoolValue(0);
	# Update last encoder position to not produce changes in the last values
	setprop("/output/EFIS/last_encoder_position", getprop("/input/arduino/EFIS/encoder-position"));
    }
};

# Set up a listener on the variable /input/arduino/EFIS/PULL_STD
setlistener("/input/arduino/EFIS/PULL_STD", toggleSTDControl, 1, 0);

var toggleAltimeterUnits = func(state) {
    var useInHg = getprop("/input/arduino/EFIS/inHG");

    if (useInHg == 1) {
        # Switch to inHg units
        setprop("/instrumentation/altimeter/inhg", 1);  # Enable inHg mode
        screen.log.write("Altimeter switched to inHg.");
    	setprop("/output/EFIS/initial_setting_inhg", getprop("/instrumentation/altimeter/setting-inhg"));
    } else {
        # Switch to hPa units
        setprop("/instrumentation/altimeter/inhg", 0);  # Disable inHg mode
        screen.log.write("Altimeter switched to hPa.");
	setprop("/output/EFIS/initial_setting_hpa", getprop("/instrumentation/altimeter/setting-hpa"));
    }

    setprop("/output/EFIS/last_encoder_position", getprop("/input/arduino/EFIS/encoder-position"));

};


# Set up a listener on the variable /input/arduino/EFIS/inHG
setlistener("/input/arduino/EFIS/inHG", toggleAltimeterUnits, 1, 0);

# Encoder
setprop("/output/EFIS/initial_setting_hpa", getprop("/instrumentation/altimeter/setting-hpa"));
setprop("/output/EFIS/initial_setting_inhg", getprop("/instrumentation/altimeter/setting-inhg"));
setprop("/output/EFIS/last_encoder_position", 0);

var handleEncoderMovement = func {

    var pull_std_active = getprop("/input/arduino/EFIS/PULL_STD");
    if (pull_std_active == 1) {
        return;  # Do nothing if STD mode is active
    }

    setprop("/output/EFIS/current_encoder_position", getprop("/input/arduino/EFIS/encoder-position"));
    var encoder_delta = getprop("/output/EFIS/current_encoder_position") - getprop("/output/EFIS/last_encoder_position");
    setprop("/output/EFIS/delta_encoder",encoder_delta);
    var use_inhg = getprop("/input/arduino/EFIS/inHG");

    if (use_inhg == 0) {
        # Mode is hPa, update setting-hpa
        var new_setting_hpa = getprop("/instrumentation/altimeter/setting-hpa") - encoder_delta;
        setprop("/instrumentation/altimeter/setting-hpa", new_setting_hpa);
    } else {
        # Mode is inHg, update setting-inhg
        var new_setting_inhg = getprop("/instrumentation/altimeter/setting-inhg") - (encoder_delta * 0.01);
        setprop("/instrumentation/altimeter/setting-inhg", new_setting_inhg);
    }
    setprop("/output/EFIS/last_encoder_position", getprop("/output/EFIS/current_encoder_position"));
};


# Set listeners to monitor encoder movements
setlistener("/input/arduino/EFIS/encoder-position", handleEncoderMovement);

var controlLhVorAdfSwitch = func {
    var signal = getprop("/input/arduino/EFIS/left-VOR-ADF");

    if (signal == 0) {
        setprop("instrumentation/efis[0]/input/lh-vor-adf", 0);  # OFF
    } else if (signal == 1) {
        setprop("instrumentation/efis[0]/input/lh-vor-adf", 1);  # VOR
    } else if (signal == -1) {
        setprop("instrumentation/efis[0]/input/lh-vor-adf", -1); # ADF
    }

    # Optionally trigger the sound if you want to replicate the sound behavior
    setprop("sim/sounde/switch1", 1);
};

# Set up a listener on the input signal variable
setlistener("/input/arduino/EFIS/left-VOR-ADF", controlLhVorAdfSwitch, 1, 0);

var controlRhVorAdfSwitch = func {
    var signal = getprop("/input/arduino/EFIS/right-VOR-ADF");

    if (signal == 0) {
        setprop("instrumentation/efis[0]/input/rh-vor-adf", 0);  # OFF
    } else if (signal == 1) {
        setprop("instrumentation/efis[0]/input/rh-vor-adf", 1);  # VOR
    } else if (signal == -1) {
        setprop("instrumentation/efis[0]/input/rh-vor-adf", -1); # ADF
    }
};

# Set up a listener on the input signal variable for right VOR-ADF
setlistener("/input/arduino/EFIS/right-VOR-ADF", controlRhVorAdfSwitch, 1, 0);

setlistener("input/arduino/EFIS/LS", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/modes/pfd/ILS1") != 1) {
            setprop("/modes/pfd/ILS1",1);
        } else {
            setprop("/modes/pfd/ILS1",0);
        }
        state.setBoolValue(0);
    }
}, 1, 0);

setlistener("input/arduino/EFIS/FD", func(state) {
    if (state.getBoolValue()) {
        if (getprop("/it-autoflight/output/fd1") != 1) {
            setprop("/it-autoflight/output/fd1",1);
        } else {
            setprop("/it-autoflight/output/fd1",0);
        }
        state.setBoolValue(0);
    }
}, 1, 0);