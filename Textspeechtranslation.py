import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = "api_key"  # input your deepl api key 

def translate_text(text, target_lang):
    """translate with deepl."""
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang,
    }
    response = requests.post(DEEPL_API_URL, data=data)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        return "translation error(mostly it is because of api errors)!"

def start_translation():
    """receive and translate audio with microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening your voice...")
        try:
            audio = recognizer.listen(source, timeout=5)
            status_label.config(text="Speech perceived, processing...")
            text = recognizer.recognize_google(audio, language=source_lang.get())
            input_text.set(text)

            # translation proccess
            translated = translate_text(text, target_lang.get())
            translated_text.set(translated)

            # audio translation output
            engine.say(translated)
            engine.runAndWait()

            status_label.config(text="Translation completed.")
        except sr.UnknownValueError:
            status_label.config(text="The speech was not understood.")
        except sr.RequestError as e:
            status_label.config(text=f"API error: {e}")
        except Exception as e:
            status_label.config(text=f"error: {e}")

# launc of text-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# tkinter interface
root = tk.Tk()
root.title("SIMPLE REAL-TIME TRANSLATION APP")
root.geometry("500x400")


LANGUAGES = {
    "Turkish": "TR",
    "English": "EN",
    "German": "DE",
    "French": "FR",
    "Spanish": "ES",
}

# ComboBox for source and target languages
source_lang_label = ttk.Label(root, text="Source Language:")
source_lang_label.pack(pady=5)
source_lang = ttk.Combobox(root, values=list(LANGUAGES.keys()))
source_lang.set("Turkish")
source_lang.pack(pady=5)

target_lang_label = ttk.Label(root, text="Target language:")
target_lang_label.pack(pady=5)
target_lang = ttk.Combobox(root, values=list(LANGUAGES.values()))
target_lang.set("EN")
target_lang.pack(pady=5)

# input and translation sections
input_text = tk.StringVar()
translated_text = tk.StringVar()

input_label = ttk.Label(root, text="Perceived Text:")
input_label.pack(pady=5)
input_entry = ttk.Entry(root, textvariable=input_text, state="readonly", width=50)
input_entry.pack(pady=5)

output_label = ttk.Label(root, text="Translation Result:")
output_label.pack(pady=5)
output_entry = ttk.Entry(root, textvariable=translated_text, state="readonly", width=50)
output_entry.pack(pady=5)

# operation button
translate_button = ttk.Button(root, text="Start", command=start_translation)
translate_button.pack(pady=20)


status_label = ttk.Label(root, text="Status: Pending")
status_label.pack(pady=10)

root.mainloop()
