/*
    MPU6050 Triple Axis Gyroscope & Accelerometer. Pitch & Roll & Yaw Gyroscope Example.
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-zyroskop-i-akcelerometr-mpu6050.html
    GIT: https://github.com/jarzebski/Arduino-MPU6050
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Timers
unsigned long timer = 0;
float timeStep = 0.01;

// Pitch, Roll and Yaw values
float pitch = 0;
float roll = 0;
float yaw = 0;

float pitch_base = 0;
float roll_base = 0;
float yaw_base = 0;

float pitch_delta = 0;
float roll_delta = 0;
float yaw_delta = 0;

float pitch_average_delta = 0;
float roll_average_delta = 0;
float yaw_average_delta = 0;

float pitch_sum = 0;
float roll_sum = 0;
float yaw_sum = 0;

float final_pitch = 0;
float final_roll = 0;
float final_yaw = 0;

int iteration_count = 0;

void setup() 
{
  Serial.begin(115200);

  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);
}

void loop()
{ 
  for (int i = 0; i <= 99; i++){
    timer = millis();
  
    // Read normalized values
    Vector norm = mpu.readNormalizeGyro();
  
    // Calculate Pitch, Roll and Yaw
    pitch = pitch + norm.YAxis * timeStep;
    roll = roll + norm.XAxis * timeStep;
    yaw = yaw + norm.ZAxis * timeStep;
  
    if (iteration_count == 0){
      pitch_base = pitch;
      roll_base = roll;
      yaw_base = yaw;
    }
    pitch_delta = pitch_base - pitch;
    roll_delta = roll_base - roll;
    yaw_delta = yaw_base - yaw;
    
    pitch_sum += pitch_delta;
    roll_sum += roll_delta;
    yaw_sum += yaw_delta;
    
    if (i == 99){
      final_pitch = pitch;
      final_roll = roll;
      final_yaw = yaw;
    }
    
    // Wait to full timeStep period
    delay((timeStep*1000) - (millis() - timer));
  }
  
  pitch_average_delta = pitch_sum/100;
  roll_average_delta = roll_sum/100;
  yaw_average_delta = yaw_sum/100;
  
  pitch_base -= pitch_average_delta;
  roll_base -= roll_average_delta;
  yaw_base -= yaw_average_delta;
  
  pitch_sum = 0;
  roll_sum = 0;
  yaw_sum = 0;
  
  iteration_count += 1;
  
  Serial.print("|");
  Serial.print("GYRO");
  Serial.print("|");
  Serial.print(final_pitch);
  Serial.print("|");
  Serial.print(final_roll);
  Serial.print("|");
  Serial.print(final_yaw);
  Serial.print("|");
  Serial.print(pitch_average_delta);
  Serial.print("|");
  Serial.print(roll_average_delta);
  Serial.print("|");
  Serial.print(yaw_average_delta);
  Serial.println("|");
  
}
