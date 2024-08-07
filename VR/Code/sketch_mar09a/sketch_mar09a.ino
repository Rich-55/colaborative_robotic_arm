#include <Servo.h>
Servo s1;
Servo s2;
void setup() {
  s1.attach(5);
  s2.attach(6);
}
void loop() {
  s1.write(77);
  s2.write(150);
  delay(15);
}
