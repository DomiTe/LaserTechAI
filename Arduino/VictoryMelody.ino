#include <IRremote.h>
#include"pitches.h"


// Define notes and melody (same as before)
int melody[] = {
    NOTE_C5, NOTE_E5, NOTE_G5, NOTE_C6, NOTE_G5, NOTE_E5, NOTE_C5, NOTE_G4, NOTE_E4, NOTE_C4
};

int noteDurations[] = {
    16, 16, 16, 8, 16, 16, 8, 16, 16, 8
};

// Pin definitions
const int irReceiverPin = 4; // Pin where the IR receiver is connected
const int buzzerPin = 3;     // Buzzer output pin

IRrecv irrecv(irReceiverPin);
decode_results results;

void setup() {
    Serial.begin(9600);           // Initialize serial communication at 9600 bits per second
    irrecv.enableIRIn();          // Start the IR receiver
    pinMode(buzzerPin, OUTPUT);   // Initialize buzzer pin as output
}

void loop() {
    if (irrecv.decode(&results)) {
        Serial.print("Received IR code: ");
        Serial.println(results.value, HEX); // Print the received IR code in hexadecimal format

        // Check if the received IR code matches your expected code
        // For example, you can use a specific IR code value to trigger the melody
       // Replace with your actual IR code value
        playVictoryMelody(); // Call function to play the victory melody

        irrecv.resume(); // Receive the next value
    }
}

void playVictoryMelody() {
    // Iterate over the notes of the melody
    for (int thisNote = 0; thisNote < sizeof(melody) / sizeof(int); thisNote++) {
        int noteDuration = 1000 / noteDurations[thisNote];
        tone(buzzerPin, melody[thisNote], noteDuration);

        // Pause between notes
        int pauseBetweenNotes = noteDuration * 1.30;
        delay(pauseBetweenNotes);

        // Stop the tone playing
        noTone(buzzerPin);
    }
}
