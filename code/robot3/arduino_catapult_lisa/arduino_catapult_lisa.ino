#include <Servo.h>

Servo servoB; // ELASTIQUE 
Servo servoLock; // RETIENT CUILLERE
Servo myservo; //tube bas
Servo myservo2;       // tube haut 

int buttonState = 0;
const int buttonPin = 7;

void setup()
{
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  servoB.attach(5);
  servoLock.attach(6);
  myservo.attach(9); 
  myservo2.attach(8); 
  resetCatapult();
}

void loop()
{
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);
  if (buttonState == HIGH)
  //|| visage == true ) ajouter ca 
 
  {
      myservo2.write(60);
  delay(50);
  myservo2.write(92); 
  delay(200);
  myservo.write(110);  //loin du tube plus c'est grand 
  delay(65);        // 1000-1 second 
  myservo.write(48); //vers l'interieur du tube plus c'est petit

    shoot();
    resetCatapult();
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
