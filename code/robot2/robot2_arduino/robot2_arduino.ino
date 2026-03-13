#define dirPin 2
#define stepPin 3
#define enablePin 4

const int THRESHOLD = 10;

bool motorActive = false;
bool lastMotorActive = false;

unsigned long lastStepTime = 0;
unsigned long stepInterval = 4000;

String inputBuffer = "";

void setup() {

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enablePin, OUTPUT);

  digitalWrite(dirPin, HIGH);
  digitalWrite(enablePin, HIGH); // start disabled

  Serial.begin(9600);

  Serial.println("Ready.");
}

void loop() {

  // -------- READ SERIAL LINE --------
  while (Serial.available() > 0) {

    char c = Serial.read();

    if (c == '\n') {

      int volume = inputBuffer.toInt();

      Serial.print("Volume: ");
      Serial.println(volume);

      inputBuffer = "";

      // -------- LOGIC --------
      if (volume < THRESHOLD) {

        // normal direction
        digitalWrite(dirPin, HIGH);
        stepInterval = 4000;
        motorActive = true;

      }
      else if (volume >= 85 && volume <= 100) {

        // reverse direction, fast
        digitalWrite(dirPin, LOW);
        stepInterval = 1200;
        motorActive = true;

      }
      else {

        motorActive = false;

      }

      // -------- STATE CHANGE --------
      if (motorActive != lastMotorActive) {

        if (motorActive) {
          Serial.println("Motor RUN");
          digitalWrite(enablePin, LOW);
        }
        else {
          Serial.println("Motor STOP");
          digitalWrite(enablePin, HIGH);
        }

        lastMotorActive = motorActive;
      }

    }
    else {
      inputBuffer += c;
    }
  }

  // -------- MOTOR STEP GENERATION --------
  if (motorActive) {

    unsigned long now = micros();

    if (now - lastStepTime >= stepInterval) {

      lastStepTime = now;

      digitalWrite(stepPin, HIGH);
      delayMicroseconds(5);
      digitalWrite(stepPin, LOW);

    }
  }
}
