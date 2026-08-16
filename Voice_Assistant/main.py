import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
from urllib.parse import quote


# -----------------------------
# Speech Recognition
# -----------------------------

recognizer = sr.Recognizer()


# -----------------------------
# Text-to-Speech
# -----------------------------

def speak(message):
    print("Assistant:", message)

    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
    engine.stop()


# -----------------------------
# Listen to User
# -----------------------------

def listen(source):

    print("\nListening... Speak now!")

    try:
        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

    except sr.WaitTimeoutError:
        # User did not speak.
        # Don't say anything; simply listen again.
        return ""

    try:
        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand you. Please repeat.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech recognition service is unavailable.")
        return ""


# -----------------------------
# Process Commands
# -----------------------------

def process_command(command):

    # Hello
    if "hello" in command:
        speak("Hello! How can I help you?")


    # Time
    elif "time" in command:

        current_time = datetime.now().strftime("%I:%M %p")

        speak(
            "The current time is "
            + current_time
        )


    # Date
    elif "date" in command:

        current_date = datetime.now().strftime("%d %B %Y")

        speak(
            "Today's date is "
            + current_date
        )


    # Web Search
    elif "search" in command:

        search_text = command.replace(
            "search",
            "",
            1
        ).strip()

        if search_text:

            speak(
                "Searching for "
                + search_text
            )

            search_url = (
                "https://www.google.com/search?q="
                + quote(search_text)
            )

            webbrowser.open(search_url)

        else:

            speak(
                "Please tell me what you want to search for."
            )


    # Good bye
    elif "good bye" in command:

        speak(
            "Thank you! I'm glad I could help."
        )


    # Exit
    elif "exit" in command or "quit" in command or "goodbye" in command:

        speak("Goodbye!")

        return False


    # Unknown command
    else:

        speak(
            "Sorry, I don't understand that command yet."
        )


    return True


# -----------------------------
# Start Voice Assistant
# -----------------------------




# -----------------------------
# Microphone
# -----------------------------

with sr.Microphone(device_index=1) as source:

    print("Adjusting for background noise...")

    recognizer.adjust_for_ambient_noise(
        source,
        duration=1
    )

    print("Voice assistant is ready!")


    # -----------------------------
    # Continuous Listening
    # -----------------------------

    while True:

        command = listen(source)

        if command:

            continue_running = process_command(
                command
            )

            if not continue_running:
                break