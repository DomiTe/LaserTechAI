import os
#from openai import OpenAI
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
from datasets import load_dataset
import sounddevice as sd
import soundfile as sf

# Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"
#client = OpenAI()
# Load the processor, model, and vocoder
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Load the speaker embeddings dataset and identify the desired speaker
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_id = 6799  # 'slt'
speaker_embeddings = torch.tensor(embeddings_dataset[speaker_id]["xvector"]).unsqueeze(0).to(device)

current_directory = os.path.dirname(os.path.abspath(__file__))

while True:

    user_text = input(">> ")

    if user_text == "exit":
        break

        # response = client.chat.completions.create(
        #     messages=[
        #         {
        #             "role": "user", "content": user_text
        #         }
        #     ], model="gpt-3.5-turbo",
        # )

    # Prepare inputs and generate speech
    inputs = processor(text=user_text, return_tensors="pt").to(device)
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    # Play the generated speech
    sd.play(speech.cpu().numpy(), 15500)
    sd.wait()

    # Save the speech to a file
    output_directory = os.path.join(current_directory, "output.wav")
    sf.write(output_directory, speech.cpu().numpy(), 15500)