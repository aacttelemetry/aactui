
/*
 * Rui Santos 
 * Complete Project Details https://randomnerdtutorials.com
 */
 
#include <TinyGPS.h> //Due to Pi limitations, this was imported as TinyGPS rather than TinyGPS++.
#include <SoftwareSerial.h>

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

void setup(){
  Serial.begin(9600);
  ss.begin(GPSBaud);
}

void loop(){
  // This sketch displays information every time a new sentence is correctly encoded.
  while (ss.available() > 0){
    gps.encode(ss.read());
    if (gps.charsProcessed() < 10){
      Serial.println("|GPS|NO_ENCODE|");
      delay(1000);
    }
    if (gps.location.isUpdated()){
      Serial.print("|");
      Serial.print("GPS");
      Serial.print("|"); 
      Serial.print(gps.location.lat(), 6);
      Serial.print("|"); 
      Serial.print(gps.location.lng(), 6);
      Serial.print("|");
      Serial.print(gps.speed.mph(),2);
      Serial.print("|");
      Serial.print(gps.course.deg(),2);
      Serial.print("|");
      Serial.print(gps.altitude.feet(),2);
      Serial.println("|");
      
    }
  }
}
