import requests
import pyttsx3
import threading
from config import GROQ_API_KEY, GROQ_API_URL

def get_groq_feedback(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    result = response.json()

    # Extract response content
    groq_response = result["choices"][0]["message"]["content"]

    # Run text-to-speech in a separate thread to avoid blocking
    threading.Thread(target=groq_output_to_speech, args=(groq_response,)).start()

    return groq_response

def groq_output_to_speech(groq_response):
    # Converts the Groq API response text to speech using pyttsx3.

    engine = pyttsx3.init()

    # Set voice properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[14].id) 
# more voices : 14, 18, 19, 

    engine.say(groq_response)
    engine.runAndWait()
