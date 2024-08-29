print("Nasal script loaded.");

var register_listener = func {
    var button_path = "/input/arduino/EFIS/button_pressed";
    setlistener(button_path, func {
        var button_name = getprop(button_path);
        if (button_name != "") {
            print("Button pressed:", button_name);
        }
    });
};

# Start the listener registration
register_listener();
print("Listener registered.");