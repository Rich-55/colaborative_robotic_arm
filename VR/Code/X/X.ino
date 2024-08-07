#include <Servo.h>
Servo s1;
Servo s2;
int X;
int pos_1 = 90;
int pos_2 = 90;
int pos_1_a;
int pos_2_a;
void setup() {
  Serial.begin(9600);
  s1.attach(5);
  s2.attach(6);
  s1.write(pos_1);
  s2.write(pos_2);
}
void loop() {
  if (Serial.available() > 0) {
    X = Serial.read();
  }
  if ( X == 1) {
    for (pos_1_a = pos_1; pos_1_a <= 180; pos_1_a += 1) {
      s1.write(pos_1_a);
    }
  }
  if ( X == 2) {
    for ( int pos_1_b = pos_1_a; pos_1_b >= 0; pos_1_b -= 1) {
      s1.write(pos_1_b);
    }
  }
  if ( X == 3) {
    for (pos_2_a = pos_1; pos_2_a <= 180; pos_2_a += 1) {
      s2.write(pos_2_a);
    }
  }
  if ( X == 4) {
    for (int pos_2_b = pos_2_a; pos_2_b >= 0; pos_2_b -= 1) {
      s2.write(pos_2_b);
    }
  }
}
