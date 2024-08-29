# Function to handle the state change of EFIS buttons
var handle_efis_button = func(button_name, property_path) {
    var state = props.globals.getNode(property_path, 1);
    
    setlistener(property_path, func {
        if (state.getBoolValue()) {
            if (button_name == "CSTR") {
                if (getprop("/instrumentation/efis/inputs/cstr") != 1) {
                    props.globals.getNode("/instrumentation/efis/inputs/cstr", 1).setBoolValue(1);
                } else {
                    props.globals.getNode("/instrumentation/efis/inputs/cstr", 1).setBoolValue(0);
                }
            } else if (button_name == "WPT") {
                if (getprop("/instrumentation/efis/inputs/wpt") != 1) {
                    props.globals.getNode("/instrumentation/efis/inputs/wpt", 1).setBoolValue(1);
                } else {
                    props.globals.getNode("/instrumentation/efis/inputs/wpt", 1).setBoolValue(0);
                }
            } else if (button_name == "VORD") {
                if (getprop("/instrumentation/efis/inputs/vord") != 1) {
                    props.globals.getNode("/instrumentation/efis/inputs/vord", 1).setBoolValue(1);
                } else {
                    props.globals.getNode("/instrumentation/efis/inputs/vord", 1).setBoolValue(0);
                }
            } else if (button_name == "NDB") {
                if (getprop("/instrumentation/efis/inputs/ndb") != 1) {
                    props.globals.getNode("/instrumentation/efis/inputs/ndb", 1).setBoolValue(1);
                } else {
                    props.globals.getNode("/instrumentation/efis/inputs/ndb", 1).setBoolValue(0);
                }
            } else if (button_name == "ARPT") {
                if (getprop("/instrumentation/efis/inputs/arpt") != 1) {
                    props.globals.getNode("/instrumentation/efis/inputs/arpt", 1).setBoolValue(1);
                } else {
                    props.globals.getNode("/instrumentation/efis/inputs/arpt", 1).setBoolValue(0);
                }
            }
            state.setBoolValue(0);  # Reset the state
        }
    }, 1, 0);
};

# Register listeners for each EFIS button
handle_efis_button("CSTR", "input/arduino/EFIS/CSTR");
handle_efis_button("WPT", "input/arduino/EFIS/WPT");
handle_efis_button("VORD", "input/arduino/EFIS/VORD");
handle_efis_button("NDB", "input/arduino/EFIS/NDB");
handle_efis_button("ARPT", "input/arduino/EFIS/ARPT");

print("EFIS button listeners registered.");
