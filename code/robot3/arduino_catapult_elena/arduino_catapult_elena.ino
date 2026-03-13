#include <Servo.h>

Servo servoB; // ELASTIQUE 
Servo servoLock; // RETIENT CUILLERE
Servo myservo; //tube bas
Servo myservo2; // tube haut

int buttonState = 0;
const int buttonPin = 7;
String inputBuffer = ""; // store incoming serial

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  
  servoB.attach(5);
  servoLock.attach(6);
  myservo.attach(9);
  myservo2.attach(8);

  resetCatapult();
}

void loop() {

  // ----------- Read BUTTON -----------
  if (digitalRead(buttonPin) == HIGH) {
    buttonState = HIGH;
  }

  // ----------- Read SERIAL safely -----------
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      inputBuffer.trim();

      if (inputBuffer == "PRESS") {
        buttonState = HIGH;
      }

      inputBuffer = "";
    } 
    else {
      inputBuffer += c;

      if (inputBuffer.length() > 50) {
        inputBuffer = "";
      }
    }
  }

  // ----------- Motor logic -----------
  if (buttonState == HIGH) {

    myservo2.write(60); //haut
    delay(70);
    myservo2.write(92);//dedans
    delay(200);

    myservo.write(110);//bas
    delay(85);
    myservo.write(50);//dedans

    shoot();
    resetCatapult();

    buttonState = LOW; // reset
  }
}

void shoot() {
  servoB.write(180);
  delay(500);
  servoLock.write(0);
  delay(500);
}

void resetCatapult() {
  servoB.write(0);
  delay(300);
  servoLock.write(180);
  delay(500);
}
