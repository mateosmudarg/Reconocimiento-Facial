void setup() {
  Serial.begin(9600); 
  pinMode(LED_BUILTIN, OUTPUT); 
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); 
    if (command == 'H') {
      digitalWrite(LED_BUILTIN, HIGH); 
    } else if (command == 'L') {
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
