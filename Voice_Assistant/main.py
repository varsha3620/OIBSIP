import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def tell_date():
    current_date = datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {current_date}")

def search_web(text):
    search_query = text.replace("search", "").strip()

    if search_query:
        speak(f"Searching for {search_query}")
        webbrowser.open(
            f"https://www.google.com/search?q={search_query}"
        )
    else:
        speak("Please tell me what you want to search for.")

with sr.Microphone() as source:
    print("Adjusting for background noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Listening... Speak now!")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    if "hello" in text.lower():
        speak("Hello! How can I help you?")

    elif "time" in text.lower():
        tell_time()

    elif "date" in text.lower():
        tell_date()
        
    elif "search" in text.lower():
        search_web(text)
except sr.UnknownValueError:
    print("Sorry, I could not understand you.")

except sr.RequestError as e:
    print("Speech recognition service is unavailable.")
    print(e)