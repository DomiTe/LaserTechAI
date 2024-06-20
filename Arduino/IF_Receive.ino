#include <IRremote.h>

const int irReceiverPin = 4; // Pin where the IR receiver is connected

IRrecv irrecv(irReceiverPin);
decode_results results;

void setup() {
  Serial.begin(9600);        // Initialize serial communication at 9600 bits per second
  irrecv.begin(irReceiverPin); // Start the IR receiver
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.print("Received IR code: ");
    Serial.println(results.value, HEX); // Print the received IR code in hexadecimal format
    irrecv.resume();                    // Receive the next value
  }
}
