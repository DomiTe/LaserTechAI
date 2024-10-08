# Talking Laser Tag Gun Project (Abondend)

## Overview
This project is a laser tag gun built using an ESP32 board, an IR transmitter and receiver, a 7-segment display for score tracking, and a buzzer for sound effects. Additionally, it incorporates speech synthesis using OpenAI GPT-3.5 and Microsoft SpeechT5 to generate and play short responses when a hit is detected or a button is pressed. 

## Features
- **IR Transmitter and Receiver**: Sends and receives IR signals for shooting and hit detection.
- **Score Tracking**: Uses a 7-segment display to show the current score (0-9).
- **Buzzer**: Plays a tone when a hit is detected or a button is pressed.
- **LED Feedback**: The built-in LED lights up when a hit is detected.
- **Speech Synthesis**: Plays sassy audio responses for certain actions using speech synthesis models.

## Hardware Components
- ESP32 Development Board
- IR Transmitter (IR LED)
- IR Receiver
- 7-Segment Display (Common Cathode)
- Shift Register (74HC595)
- Buzzer
- Push Buttons (for sending IR signals and resetting the score)
- Built-in LED (or external if preferred)

## Pin Configuration
- **IR_RECEIVER_PIN**: GPIO 15
- **IR_LED_PIN**: GPIO 16
- **SEND_BUTTON_PIN**: GPIO 5
- **RESET_BUTTON_PIN**: GPIO 4
- **BUZZER_PIN**: GPIO 17
- **LED_PIN**: GPIO 2 (Built-in)
- **DATA_PIN**: GPIO 18 (For the shift register)
- **CLOCK_PIN**: GPIO 19 (For the shift register)
- **LATCH_PIN**: GPIO 21 (For the shift register)

## Software Setup

### Dependencies:
1. Arduino IDE installed with ESP32 board support.
2. Libraries:
   - `IRremoteESP8266` for handling IR communication.
   - Python packages for speech synthesis: `torch`, `transformers`, `sounddevice`, `soundfile`, and `openai`.

### Arduino Code

- The main program detects IR signals, tracks scores, and controls the 7-segment display, LED, and buzzer.
- The gun can shoot IR signals when the "SEND" button is pressed.
- A hit is detected when an IR signal is received, and the score increments accordingly.
- Pressing the "RESET" button resets the score to 0.

### Speech Synthesis Code
- This project uses OpenAI's GPT-3.5 and Microsoft SpeechT5 models to generate speech when the Arduino sends specific serial messages to the host computer.
- The program listens for serial input from the Arduino (e.g., when a hit is detected) and plays a short, fun audio response.

### Steps to Set Up:
1. Upload the Arduino code to your ESP32 board.
2. Run the Python script for speech synthesis on your PC. Ensure all necessary libraries are installed, and the ESP32 is connected via the correct serial port.
3. The Python script listens to the serial input from the Arduino and plays generated responses using a speaker or headphones.

## How to Use
1. **Start the game**: Power on the ESP32, and the score will be displayed as 0.
2. **Shoot**: Press the "SEND" button to send an IR signal and play a tone.
3. **Hit Detection**: When the IR receiver detects a hit, the score increases by 1, the LED lights up, and a tone plays.
4. **Speech**: If connected to the speech synthesis system, the system will generate a short spoken phrase when a hit is detected.
5. **Reset**: Press the "RESET" button to reset the score.

## Possible Future Enhancements
- Extend the speech system to recognize different events (e.g., low score, high score).
- Use a multi-digit display to handle scores beyond 9.
- Add more complex sound effects and voice lines.
