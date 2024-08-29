#include "Adafruit_seesaw.h"

/////////////////////////  BOTONES ///////////////////////////
// Por ahora con lectura digitales en loop, más tarde se puede realizar una lectura en rutina de interrupción usando los diodos
const int bump_time = 250;
const int num_buttons = 7;
                        //CSTR,WPT,VORD, NDB, ARPT,         botones_2
const int buttons  [] = {38, 36, 24, 30, 28, 44, 48};
bool state_buttons [] = { 0,  0,  0,  0,  0,  0,  0};
bool press_event = 0;
unsigned long press_time = 100;

//////////////////////// SWITCHES ///////////////////////
                        //12 pos, 3 pos 
const int switches [] = {A1, A0, A2, A3};
int state_switches [] = { 0,  0,  0,  0};


////////////////////// CONMUTADORES ENCODER /////////////////////////
// de izq a derecha [~Hg/hPa, ~PUSH/PULL]
const int num_conmute = 2;
const int conmute  [] = {23, 25}; 
bool state_conmute [] = { 0,  0};

///////////////////// ENCODERS /////////////////////////////
#define SEESAW_ADDR          0x36

Adafruit_seesaw ss;
int32_t encoder_position;

///////////////////// LEDS /////////////////////////////
                    //botones_5,        botones_2
const int led [] = {40, 34, 22, 32, 26, 42, 46};

unsigned long t_send = 0;
const int fr = 100;
/////////////////////////////////////////////// SETUP //////////////////////////////////////////////////////////////////////////////////
void setup() {
  Serial.begin(1000000);
  while (!Serial) delay(10);

  if (! ss.begin(SEESAW_ADDR)) {
    while(1) delay(10);
  }
  encoder_position = ss.getEncoderPosition();
  ss.enableEncoderInterrupt();

  for (int i = 0 ; i<7; i++){
    pinMode (led[i], OUTPUT);
  }
  delay(100);
}
////////////////////////////////////////////// LOOP ///////////////////////////////////////////////////////////////////////////////////
void loop() {
  func_buttons();
  func_encoder();
  func_switches();
  if (millis()> t_send+fr){
    t_send = millis();
    func_conmute();
    envio();
    lectura();
    memset(state_buttons, 0, num_buttons);
  }
}

////////////////////////////////////////////// FUNCTIONS ////////////////////////////////////////////////////////////////////////////////
void lectura() {
  while(Serial.available() != 0){
    String data = Serial.readStringUntil('\n');
    if (data.length() == 7) {
      //all variables
      digitalWrite(led[0],data.substring(0,1) == "1");
      digitalWrite(led[1],data.substring(1,2) == "1");
      digitalWrite(led[2],data.substring(2,3) == "1");
      digitalWrite(led[3],data.substring(3,4) == "1");
      digitalWrite(led[4],data.substring(4,5) == "1");
      digitalWrite(led[5],data.substring(5,6) == "1");
      digitalWrite(led[6],data.substring(6,7) == "1");
    } else if(data.length() == 6) {
      //no LS button
      digitalWrite(led[0],data.substring(0,1) == "1");
      digitalWrite(led[1],data.substring(1,2) == "1");
      digitalWrite(led[2],data.substring(2,3) == "1");
      digitalWrite(led[3],data.substring(3,4) == "1");
      digitalWrite(led[4],data.substring(4,5) == "1");
      digitalWrite(led[5],data.substring(5,6) == "1");
    }else{
      // no LS and FD buttons
      digitalWrite(led[0],data.substring(0,1) == "1");
      digitalWrite(led[1],data.substring(1,2) == "1");
      digitalWrite(led[2],data.substring(2,3) == "1");
      digitalWrite(led[3],data.substring(3,4) == "1");
      digitalWrite(led[4],data.substring(4,5) == "1");
    }

  }
}

void envio() {
  char buffer[80];
  //specified format below uses 31 characters: 2 brackets + 13 comas + 3 digits encoder + 7 buttons + 4 switches+ 2 conmuters
  sprintf(buffer, "{%+05ld,%d,%d,%d,%d,%d,%d,%d,%d,%d,%+02d,%+02d,%d,%d}", \
    encoder_position, \
    state_buttons [0], state_buttons [1], state_buttons [2], state_buttons [3], state_buttons [4], state_buttons [5], state_buttons [6],  \
    state_switches [0], state_switches [1], state_switches [2], state_switches [3], \
    state_conmute [0], state_conmute [1]);

  Serial.println(buffer);
}

void func_buttons() {
  if (millis() > press_time + bump_time){ 
    int i = 0;
    press_event = 0;
    while (i<7 && !press_event){
      if(digitalRead(buttons[i])==1){
        press_time = millis();
        state_buttons[i] = 1;
        press_event = 1;
      }
      else{
       i++;
      }
    }
  }
}

void func_conmute() {
  state_conmute [0]= digitalRead(conmute [0]);
  state_conmute [1]= !digitalRead(conmute [1]);
}

void func_encoder() {
  int32_t new_position = ss.getEncoderPosition();
  // did we move around?
  if (encoder_position != new_position) {
    encoder_position = new_position;      // and save for next round
    delay(10);
  }
}

void func_switches(){

  // Read analog values from the pins defined in switches array and store in state_switches array
  for (int i = 0; i < 4; i++) {
    state_switches[i] = analogRead(switches[i]);
  }

  // Switch_12P_1 (state_switches[0])
  if (state_switches[0] > 550) {
      state_switches[0] = 1;
  } else if (state_switches[0] > 500 && state_switches[0] <= 550) {
      state_switches[0] = 2;
  } else if (state_switches[0] > 425 && state_switches[0] <= 500) {
      state_switches[0] = 3;
  } else if (state_switches[0] > 350 && state_switches[0] <= 425) {
      state_switches[0] = 4;
  } else if (state_switches[0] > 225 && state_switches[0] <= 350) {
      state_switches[0] = 5;
  } else {
      state_switches[0] = 5;
  }

  // Switch_12P_2 (state_switches[1])
  if (state_switches[1] > 550) {
      state_switches[1] = 1;
  } else if (state_switches[1] > 500 && state_switches[1] <= 550) {
      state_switches[1] = 2;
  } else if (state_switches[1] > 425 && state_switches[1] <= 500) {
      state_switches[1] = 3;
  } else if (state_switches[1] > 350 && state_switches[1] <= 425) {
      state_switches[1] = 4;
  } else if (state_switches[1] > 225 && state_switches[1] <= 350) {
      state_switches[1] = 5;
  } else {
      state_switches[1] = 6;
  }

  // Switch_3P_1 (state_switches[2])
  if (state_switches[2] < 341) {
      state_switches[2] = -1;
  } else if (state_switches[2] < 682) {
      state_switches[2] = 1;
  } else {
      state_switches[2] = 0;
  }

  // Switch_3P_2 (state_switches[3])
  if (state_switches[3] < 341) {
      state_switches[3] = -1;
  } else if (state_switches[3] < 682) {
      state_switches[3] = 1;
  } else {
      state_switches[3] = 0;
  }
}


//////////////////////////////////////////////////// INTERRUPTIONS /////////////////////////////////////////////////////////////////////////
/*
void read_buttons () {
  for (int i = 0; i < 8; i++) {
    state_buttons[i] = digitalRead(buttons[i]);
  }
}
*/