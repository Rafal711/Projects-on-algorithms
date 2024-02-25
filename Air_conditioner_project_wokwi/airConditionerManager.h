enum IR_RemoteButtons {
      POWER = 162,
      MENU = 226,
      TEST = 34,
      PLUS = 2,
      BACK = 194,
      PREV = 224,
      PLAY = 168,
      NEXT = 144,
      num_0 = 104,
      MINUS = 152,
      key_C = 176,
      num_1 = 48,
      num_2 = 24,
      num_3 = 122,
      num_4 = 16,
      num_5 = 56,
      num_6 = 90,
      num_7 = 66,
      num_8 = 74,
      num_9 = 82
};


typedef enum {
  COOL,
  WIND,
  HEAT
} AirConditionerMode;

const char* acMode2Str(AirConditionerMode ac_mode) {
    switch (ac_mode) {
    case COOL:
      return "COOL";
    case WIND:
      return "WIND";
    case HEAT:
      return "HEAT";
    default:
      return "N/A";
  }
}

typedef enum {
  OFF,
  ON
} AirConditionerStatus;

const char* acStatus2Str(AirConditionerStatus ac_status) {
  switch (ac_status) {
    case OFF:
      return "OFF";
    case ON:
      return "ON";
    default:
      return "N/A";
  }
}

typedef enum {
  MANUAL,
  AUTOMATIC
} AirConditionerRegulation;

const char* acRegulation2Str(AirConditionerRegulation regulation) {
  switch (regulation) {
    case MANUAL:
      return "MANUAL";
    case AUTOMATIC:
      return "AUTO";
    default:
      return "N/A";
  }
}

typedef struct AirConditionerParams {
  AirConditionerStatus status; // ON/OFF
  float set_temperature;
  unsigned int set_ventilation_power;
  AirConditionerMode mode;
  AirConditionerRegulation regulation;
} AirConditionerParams;


void handle_power(AirConditionerParams* airConditionerParams) {
  switch (airConditionerParams->status) {
    case OFF:
      airConditionerParams->status = ON;
      break;
    case ON:
      airConditionerParams->status = OFF;
      break;
    default:
      break;
  }
}

void handle_temperature_turn_up(AirConditionerParams* airConditionerParams) {
  airConditionerParams->set_temperature += 0.5;
}

void handle_temperature_turn_down(AirConditionerParams* airConditionerParams) {
  airConditionerParams->set_temperature -= 0.5;
}

void handle_ventilationPower_turn_up(AirConditionerParams* airConditionerParams) {
  if (airConditionerParams->set_ventilation_power < 100) {
    airConditionerParams->set_ventilation_power += 10;
  }
}

void handle_ventilationPower_turn_down(AirConditionerParams* airConditionerParams) {
  if (airConditionerParams->set_ventilation_power > 10) {
    airConditionerParams->set_ventilation_power -= 10;
  }
}

void handle_cooling(AirConditionerParams* airConditionerParams) {
  airConditionerParams->mode = COOL;
}

void handle_wind(AirConditionerParams* airConditionerParams) {
  airConditionerParams->mode = WIND;
}

void handle_heating(AirConditionerParams* airConditionerParams) {
  airConditionerParams->mode = HEAT;
}

void handle_regulation_mode(AirConditionerParams* airConditionerParams) {
  if (airConditionerParams->regulation == MANUAL) {
    airConditionerParams->regulation = AUTOMATIC;
  }
  else {
    airConditionerParams->regulation = MANUAL;
  }

}

void handle_air_conditioning(IRrecv* receiver, AirConditionerParams* airConditionerParams) {
  if (!receiver) {
    Serial.println("IR ERROR\n");
    return;
  }

  if (!airConditionerParams) {
    Serial.println("air-conditioner parameters ERROR\n");
    return;
  }

  if (receiver->decodedIRData.command == POWER) {
    handle_power(airConditionerParams);
    return;
  }

  if (airConditionerParams->status == OFF) {
    return;
  }

  switch (receiver->decodedIRData.command) {
    case TEST: // plus temp
      handle_temperature_turn_up(airConditionerParams); 
      break;
    case num_0: // minus temp
      handle_temperature_turn_down(airConditionerParams);
      break;
    case PLUS: // HEAT
      handle_heating(airConditionerParams);
      break;
    case PLAY: // WIND
      handle_wind(airConditionerParams);
      break;
    case MINUS: // COOL
      handle_cooling(airConditionerParams);
      break;
    case BACK: // plus power
      handle_ventilationPower_turn_up(airConditionerParams); 
      break;
    case key_C: // minus power
      handle_ventilationPower_turn_down(airConditionerParams);
      break;
    case MENU: // regulation mode
      handle_regulation_mode(airConditionerParams);
      break;
    default:
      Serial.println("Not Implemented\n");
      break;
  }
}
