# Function to format the HPA setting as a 4-digit integer
var format_hpa = func(val) {
    return sprintf("%04d", val);
};

# Function to format the inHg setting to "00.00" format
var format_inhg = func(val) {
    return sprintf("%.2f", val);
};

# Combined function to update both HPA and inHg settings
var updateEFISSettings = func {
    # Update the formatted HPA setting
    var setting_hpa = getprop("/instrumentation/altimeter/setting-hpa");
    var formatted_setting_hpa = format_hpa(setting_hpa);
    setprop("/output/EFIS/formatted-setting-hpa", formatted_setting_hpa);
    
    # Update the formatted inHg setting
    var setting_inhg = getprop("/instrumentation/altimeter/setting-inhg");
    var formatted_setting_inhg = format_inhg(setting_inhg);
    setprop("/output/EFIS/formatted-setting-inhg", formatted_setting_inhg);
};

# Attach a single listener to the /input/arduino/EFIS/update-screen-EFIS property
setlistener("/input/arduino/EFIS/update-screen-EFIS", updateEFISSettings);