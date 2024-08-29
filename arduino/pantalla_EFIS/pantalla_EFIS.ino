#include <Arduino.h>
#include <U8g2lib.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

// Pin Definitions
uint8_t PIN_CS_1 = 22;
uint8_t PIN_RES_1 = 29;
uint8_t PIN_DC = 2;

// Global Variables for Display
bool altimeter_std = 0;
bool altimeter_inHg = 0;
bool s = 0;
unsigned short int altitude_hpa = 0;
float altitude_inhg = 0.00;

U8G2_SH1106_128X64_NONAME_F_4W_HW_SPI disp1(U8G2_R0, PIN_CS_1, PIN_DC, PIN_RES_1);

void setup() {
  // Initialize Serial Communication
  Serial.begin(115200);
  Serial.setTimeout(25);

  // Initialize Display
  disp1.begin();

  delay(10); // Stabilization delay
}

// Function to Update the Display based on received data
void updateDisplay(bool altimeter_std, bool altimeter_inHg, unsigned short int altitude_hpa, float altitude_inhg) {
    disp1.clearBuffer();

    if (altimeter_std) {
        disp1.setFont(u8g2_font_logisoso34_tf);  // Switch to a font that supports letters for "Std"
        disp1.drawStr(30, 50, "Std");  // Adjust position for best visibility
    } else {
        if (altimeter_inHg) {
            disp1.setFont(u8g2_font_7_Seg_41x21_mn);
            char buffer[6];
            dtostrf(altitude_inhg, 5, 2, buffer);  // Convert float to string with 2 decimal places
            disp1.drawStr(0, 12, buffer);  // Display the number with the correct font
        } else {
            // Use the 7-segment font for hPa
            disp1.setFont(u8g2_font_7Segments_26x42_mn);
            disp1.drawStr(0, 48, String(altitude_hpa).c_str());  // Display hPa value
        }
    }

    disp1.sendBuffer();
}



void loop() {
  // Wait for incoming data
  while (Serial.available() == 0) {}

  // Read the incoming data
  String data = Serial.readStringUntil('\n');

  // Parse the received data for display
  altimeter_std = data.substring(0, 1) == "1";
  altimeter_inHg = data.substring(1, 2) == "1";
  altitude_hpa = data.substring(2, 6).toInt();
  altitude_inhg = data.substring(6, 11).toFloat();
  s = data.substring(11, 12) == "1";

  // Update the display based on the parsed data
  updateDisplay(altimeter_std, altimeter_inHg, altitude_hpa, altitude_inhg);
}
