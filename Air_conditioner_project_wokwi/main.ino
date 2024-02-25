#include "DHT.h"
#include <Wire.h>
#include <IRremote.h>
#include <LiquidCrystal_I2C.h>
#include "airConditionerManager.h"

#define DELAY_MS 500 // Loop delay [ms]


//PINS
#define PIN_RECEIVER A0
#define DHTPIN 12     
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
#define STATUS_LED_PIN 8

#define RGB_RED 11    //
#define RGB_GREEN 10  // RGB LED pinsS
#define RGB_BLUE 9    //


// temperature and humidity sensor initialization
DHT dht(DHTPIN, DHTTYPE);

// IR receiver initialization
IRrecv receiver(PIN_RECEIVER);

// LCD screen initialization
LiquidCrystal_I2C LCD(0x27, 20, 4);

// AC parameters initialization
AirConditionerParams airConditionerParams = {OFF, 20.0, 50, WIND, MANUAL};

float DHT_temperature_C;
float DHT_humidity;


void setup() {
  Serial.begin(115200);
  Serial.println("Started!");

  dht.begin();

  LCD.init();

  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  receiver.enableIRIn(); // Start the receiver

  change_target_AC_status(airConditionerParams.status);
  change_target_AC_mode(airConditionerParams.mode);

}


float hysteresis = 2.0;
bool output = 0;

void calc_regulator_output(AirConditionerParams* ac_params, float sensor_temperature){

    float error = ac_params->set_temperature - sensor_temperature;

    if (ac_params->mode == COOL){
      if (error > hysteresis / 2 && output == 1) {
        output = 0;
      }
      if (error < -hysteresis / 2 && output == 0) {
        output = 1;
      }
    }
    else if (ac_params->mode == HEAT){
      if (error > hysteresis / 2 && output == 0) {
        output = 1;
      }
      if (error < -hysteresis / 2 && output == 1) {
        output = 0;
      }
    }
    else {
      output = 1;
    }
}

// AC status (ON/OFF) simulated with green LED
void change_target_AC_status(AirConditionerStatus ac_status) {
  if(ac_status == ON) {
    digitalWrite(STATUS_LED_PIN, HIGH);
  }
  else { // ac_status == OFF
    digitalWrite(STATUS_LED_PIN, LOW);
  }
}

void change_target_AC_mode(AirConditionerMode ac_mode) {
  if (ac_mode == WIND) {
    set_RGB(255, 255, 255);  
  }
  else if (ac_mode == HEAT) {
    set_RGB(255, 0, 0);
  }
  else { // ac_mode == COOL
    set_RGB(0, 0, 255);
  }
}

void set_RGB(int red_brightness, int green_brightness, int blue_brightness){
  analogWrite(RGB_RED, red_brightness);
  analogWrite(RGB_GREEN, green_brightness);
  analogWrite(RGB_BLUE, blue_brightness);
}

void handle_display(AirConditionerParams* ac_params) {

  if (!ac_params) {
    Serial.println("AirConditioner parameters ERROR!");
  }

  // AC status in first row
  LCD.setCursor(0, 0);
  if (ac_params->regulation == AUTOMATIC) {
    LCD.print("POWER [%]: "); LCD.print(ac_params->set_ventilation_power * output); LCD.print(" ");
  } 
  else {
    LCD.print("POWER [%]: "); LCD.print(ac_params->set_ventilation_power); LCD.print(" ");
  }

  // Regulation mode in second row
  LCD.setCursor(0, 1);
  LCD.print("REGULATION: "); LCD.print(acRegulation2Str(ac_params->regulation)); LCD.print("  ");
  

  if (isnan(DHT_temperature_C) || isnan(DHT_humidity)) {
    Serial.println("Error while reading temperature and humidity measurements!");
  }
  else
  {
    // Current temperature in third row
    LCD.setCursor(0, 2);
    LCD.print("CURR TEMP [C]: "); LCD.print(DHT_temperature_C);

    if (ac_params->regulation == AUTOMATIC) {
      // AC set temperature in second row
      LCD.setCursor(0, 3);
      LCD.print("SET TEMP [C]: "); LCD.print(ac_params->set_temperature);
    }
    else {
      LCD.setCursor(0, 3);
      LCD.print("                    ");
    }
  }

}

void loop() {

  DHT_temperature_C = dht.readTemperature();

  AirConditionerStatus prev_status = airConditionerParams.status;
  AirConditionerMode prev_mode = airConditionerParams.mode;

  // Checks received an IR signal
  if (receiver.decode()) {
    handle_air_conditioning(&receiver, &airConditionerParams);
    receiver.resume();  // Receive the next value
  }

  if (airConditionerParams.regulation == AUTOMATIC) {
    calc_regulator_output(&airConditionerParams, DHT_temperature_C);
  }

  if (airConditionerParams.status != prev_status) {
    change_target_AC_status(airConditionerParams.status);
  }

  if (airConditionerParams.mode != prev_mode) {
    change_target_AC_mode(airConditionerParams.mode);
  }

  if (airConditionerParams.status == ON) {
    if (prev_status == OFF) {LCD.backlight();}
    handle_display(&airConditionerParams);
  }
  else {
    if (prev_status == ON) {
      LCD.clear();
      LCD.noBacklight();
    }
  }

  delay(DELAY_MS);
}
