var setEfisOptions = func(n, a, b, c, d, e, f) {
    props.globals.getNode("/instrumentation/efis/inputs/arpt", true).setBoolValue(a);
    props.globals.getNode("/instrumentation/efis/inputs/cstr", true).setBoolValue(b);
    props.globals.getNode("/instrumentation/efis/inputs/dme", true).setBoolValue(c);
    props.globals.getNode("/instrumentation/efis/inputs/ndb", true).setBoolValue(d);
    props.globals.getNode("/instrumentation/efis/inputs/vord", true).setBoolValue(e);
    props.globals.getNode("/instrumentation/efis/inputs/wpt", true).setBoolValue(f);
};

var handle_custom_button = func(button_name) {
    print("Button pressed:", button_name);
    if (button_name == "CSTR") {
        if (getprop("/instrumentation/efis/inputs/cstr") != 1) {
            setEfisOptions(0, 1, 0, 0, 0, 0, 0);
        } else {
            setEfisOptions(0, 0, 0, 0, 0, 0, 0);
        }
    } else if (button_name == "WPT") {
        if (getprop("/instrumentation/efis/inputs/wpt") != 1) {
            setEfisOptions(0, 0, 0, 0, 0, 0, 1);
        } else {
            setEfisOptions(0, 0, 0, 0, 0, 0, 0);
        }
    } else if (button_name == "VORD") {
        if (getprop("/instrumentation/efis/inputs/vord") != 1) {
            setEfisOptions(0, 0, 0, 1, 0, 1, 0);
        } else {
            setEfisOptions(0, 0, 0, 0, 0, 0, 0);
        }
    } else if (button_name == "NDB") {
        if (getprop("/instrumentation/efis/inputs/ndb") != 1) {
            setEfisOptions(0, 0, 0, 0, 1, 0, 0);
        } else {
            setEfisOptions(0, 0, 0, 0, 0, 0, 0);
        }
    } else if (button_name == "ARPT") {
        if (getprop("/instrumentation/efis/inputs/arpt") != 1) {
            setEfisOptions(1, 0, 0, 0, 0, 0, 0);
        } else {
            setEfisOptions(0, 0, 0, 0, 0, 0, 0);
        }
    }
};

var register_listener = func {
    var button_path = "/input/arduino/EFIS/button_pressed";
    setlistener(button_path, func {
        var button_name = getprop(button_path);
        if (button_name != "") {
            handle_custom_button(button_name);
        }
    });
};

# Start the listener registration
register_listener();
print("Nasal script initialized and listener registered.");
