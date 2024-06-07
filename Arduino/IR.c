#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

// Define the pins
const int IR_RECEIVER_PIN = 15;
const int IR_LED_PIN = 16;
const int SEND_BUTTON_PIN = 5;
const int RESET_BUTTON_PIN = 4;
const int BUZZER_PIN = 17;
const int LED_PIN = 2; // Built-in LED on most ESP32 boards
const int DATA_PIN = 18;
const int CLOCK_PIN = 19;
const int LATCH_PIN = 21;

// Variables to keep track of the score
int score = 0;
bool hitDetected = false;

// IR transmitter setup
IRsend irsend(IR_LED_PIN);

// Segment codes for 0-9 digits on a common cathode 7-segment display
const byte segmentCodes[] = {
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111101, // 6
  0b00000111, // 7
  0b01111111, // 8
  0b01101111  // 9
};

void setup() {
  // Initialize the serial communication
  Serial.begin(115200);
  
  // Set the IR receiver, button, and display pins as input/output
  pinMode(IR_RECEIVER_PIN, INPUT);
  pinMode(SEND_BUTTON_PIN, INPUT_PULLUP);
  pinMode(RESET_BUTTON_PIN, INPUT_PULLUP); // Assuming the button connects to GND when pressed
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);

  // Initialize the IR transmitter
  irsend.begin();

  // Turn off the LED initially
  digitalWrite(LED_PIN, LOW);
  
  // Print initial score
  Serial.print("Score: ");
  Serial.println(score);
  // Display the initial score
  displayScore(score);
}

void playSound() {
  // Play a simple tone
  tone(BUZZER_PIN, 1000); // Play a 1000 Hz tone
  delay(200); // Wait for 200 ms
  noTone(BUZZER_PIN); // Stop the tone
}

void displayScore(int score) {
  // Ensure the score is within 0-9 range for single digit display
  if (score < 0) score = 0;
  if (score > 9) score = 9;
  
  // Get the corresponding segment code
  byte segments = segmentCodes[score];
  
  // Send the segments to the shift register
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, LSBFIRST, segments);
  digitalWrite(LATCH_PIN, HIGH);
}

void loop() {
  // Read the state of the IR receiver
  int irValue = digitalRead(IR_RECEIVER_PIN);
  
  // Check if the IR receiver has detected an IR signal
  if (irValue == LOW) { // Assuming the receiver outputs LOW when detecting IR
    if (!hitDetected) {
      hitDetected = true; // Mark the hit as detected to avoid multiple counts for the same hit
      score++; // Increment the score
      Serial.print("Hit detected! Score: ");
      Serial.println(score);
      
      // Turn on the LED
      digitalWrite(LED_PIN, HIGH);
      
      // Display the score
      displayScore(score);
    }
  } else {
    hitDetected = false; // Reset the hit detection flag when no signal is detected
    
    // Turn off the LED
    digitalWrite(LED_PIN, LOW);
  }
  
  // Check if the send button is pressed
  if (digitalRead(SEND_BUTTON_PIN) == LOW) { // Assuming the button is active low
    // Send an IR signal (e.g., a NEC protocol signal with a sample command)
    irsend.sendNEC(0x20DF10EF, 32); // Example NEC command: Replace with your desired command
    Serial.println("IR signal sent!");
    
    // Play sound
    playSound();
    
    // Wait for the button to be released to avoid multiple sends
    while (digitalRead(SEND_BUTTON_PIN) == LOW) {
      delay(10);
    }
  }
  
  // Check if the reset button is pressed
  if (digitalRead(RESET_BUTTON_PIN) == LOW) { // Assuming the button is active low
    score = 0; // Reset the score
    Serial.println("Score reset!");
    
    // Display the score
    displayScore(score);
    
    // Wait for the button to be released to avoid multiple resets
    while (digitalRead(RESET_BUTTON_PIN) == LOW) {
      delay(10);
    }
  }
  
  // Small delay to avoid flooding the serial monitor
  delay(100);
}
