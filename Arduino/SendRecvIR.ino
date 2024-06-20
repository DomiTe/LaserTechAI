#include <IRremote.h>

const int recvPin = 4;    // Pin where the IR receiver is connected
const int ledPin = 13;    // Built-in LED pin
const int sendPin = 3;    // Pin where the IR LED is connected
const int buttonPin = 2;  // Pin where the button is connected

uint8_t sCommand = 0x34;
uint8_t sRepeats = 0;

IRrecv irrecv(recvPin);
IRsend irsend;
decode_results results;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Set button pin as input with internal pull-up resistor
  Serial.begin(9600); // Initialize serial communication at 9600 bits per second
  irrecv.enableIRIn(); // Start the receiver
  IrSender.begin(sendPin);
}

void loop() {
  // Check if IR signal is received
  if (irrecv.decode(&results)) {
    Serial.println("greeting");
    digitalWrite(ledPin, HIGH); // Turn on the LED
    delay(1000); // Keep the LED on for a second
    digitalWrite(ledPin, LOW); // Turn off the LED
    irrecv.resume(); // Receive the next value
  }

  // Check if the button is pressed
  if (digitalRead(buttonPin) == LOW) { // Button pressed (active low)
    // Example: Send a NEC signal with a specific code
    IrSender.sendNEC(0x00, sCommand, sRepeats);
    Serial.println("Fired!");
    }

    digitalWrite(ledPin, HIGH); // Turn on the LED as feedback
    delay(500); // Short delay for feedback
    digitalWrite(ledPin, LOW); // Turn off the LED
  
}
