import os
import serial
import asyncio
import openai
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
from datasets import load_dataset
import sounddevice as sd
import soundfile as sf

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
openai.api_key = ""

# Load the processor, model, and vocoder
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Load the speaker embeddings dataset and identify the desired speaker
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_id = 6799 #slt
speaker_embeddings = torch.tensor(embeddings_dataset[speaker_id]["xvector"]).unsqueeze(0).to(device)

# Flag to indicate if a response is being processed
is_processing_response = False


async def process(activity):
    global is_processing_response

    activity_prompts = {
        "greeting": "Give me a short (max. 10 Words) and sassy praise to why I hit my target with the laser gun.",
    }

    if activity in activity_prompts:
        user_text = activity_prompts[activity]
    else:
        user_text = "I'm not sure what you want."

    try:
        print(f"Requesting response for: {activity}")
        response = await asyncio.to_thread(openai.completions.create,
                                           model="gpt-3.5-turbo-instruct",
                                           prompt=user_text,
                                           max_tokens=20)
        chatgpt_response = response.choices[0].text.strip()

        # Prepare inputs and generate speech
        inputs = processor(text=chatgpt_response, return_tensors="pt").to(device)
        with torch.no_grad():
            speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

        # Play the generated speech
        print("Playing response...")
        sd.play(speech.cpu().numpy(), 15500)
        sd.wait()
        print("Response played!")

        # (Optional) Save the speech to a file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.join(current_directory, "output.wav")
        sf.write(output_directory, speech.cpu().numpy(), 15500)

        print("Response saved to output.wav")
        print("Response:", chatgpt_response)

    except Exception as e:
        print(f"Error processing or playing response: {e}")
    finally:
        is_processing_response = False

async def main():
    global is_processing_response
    
    arduino = serial.Serial('COM6', 9600, timeout=1)
    print("Connected")
    
    while True:
        while not is_processing_response and arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').rstrip()
            print("Received data from Arduino:", data)
            if data == "greeting":
                is_processing_response = True
                await process('greeting')

if __name__ == '__main__':
    asyncio.run(main())
