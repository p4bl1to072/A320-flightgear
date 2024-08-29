# udp-fcu-in.nas

var setEfisOptions = func(n, a, b, c, d, e, f) {
    pts.Instrumentation.Efis.Inputs.arpt[n].setBoolValue(a);
    pts.Instrumentation.Efis.Inputs.cstr[n].setBoolValue(b);
    pts.Instrumentation.Efis.Inputs.dme[n].setBoolValue(c);
    pts.Instrumentation.Efis.Inputs.ndb[n].setBoolValue(d);
    pts.Instrumentation.Efis.Inputs.vord[n].setBoolValue(e);
    pts.Instrumentation.Efis.Inputs.wpt[n].setBoolValue(f);
};

var handle_custom_button = func(button_name) {
    if (button_name == "CSTR") {
        cpt_efis_btns("cstr");
    } else if (button_name == "WPT") {
        cpt_efis_btns("wpt");
    } else if (button_name == "VORD") {
        cpt_efis_btns("vord");
    } else if (button_name == "NDB") {
        cpt_efis_btns("ndb");
    } else if (button_name == "ARPT") {
        cpt_efis_btns("arpt");
    } else if (button_name == "OFF") {
        cpt_efis_btns("off");
    }
};

var register_listener = func {
    var button_path = "/input/arduino/EFIS/button_pressed";
    setlistener(button_path, func {
        var button_name = getprop(button_path);
        handle_custom_button(button_name);
    });
};

# Start the listener registration
register_listener();
