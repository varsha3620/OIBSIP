import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
from urllib.parse import quote
from nlp import predict_intent
from weather import get_weather
from reminder import set_reminder
from email_sender import send_email
from knowledge import answer_question
from custom_commands import execute_custom_command
# -----------------------------
# Speech Recognition
# -----------------------------

recognizer = sr.Recognizer()
reminder_speaking = False

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
            phrase_time_limit=8
        )

    except sr.WaitTimeoutError:
        # User did not speak.
        # Stay silent and listen again.
        return ""

    try:
        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech recognition service is unavailable.")
        return ""



# -----------------------------
# Search Web
# -----------------------------

def search_web(command):

    search_words = [
        "search",
        "look up",
        "lookup",
        "find",
        "find information about",
        "find information on",
        "look for",
        "search the web for",
        "search online for"
    ]

    search_text = command.lower()

    for phrase in search_words:
        if phrase in search_text:
            search_text = search_text.replace(phrase, "", 1)
            break

    # Remove unnecessary words
    unnecessary_words = [
        "can you",
        "could you",
        "please",
        "for me",
        "the"
    ]

    for phrase in unnecessary_words:
        search_text = search_text.replace(phrase, "")

    search_text = " ".join(search_text.split())

    if search_text:

        speak("Searching for " + search_text)

        search_url = (
            "https://www.google.com/search?q="
            + quote(search_text)
        )

        webbrowser.open(search_url)

    else:

        speak("Please tell me what you want to search for.")

# -----------------------------
# Weather Command
# -----------------------------
def weather_command(command, source):

    weather_words = [
        "weather in",
        "weather at",
        "weather for"
    ]

    city = ""

    # Check if city is already in the command
    for phrase in weather_words:

        if phrase in command:

            city = command.split(phrase, 1)[1].strip()
            break

    # If city was not included, ask for it
    if not city:

        speak("Which city would you like the weather for?")

        city = listen(source)

        if not city:
            return

    # Get weather
    weather_result = get_weather(city)

    speak(weather_result)

# -----------------------------
# Create Reminder
# -----------------------------

def create_reminder(command):

    words = command.split()

    seconds = 0

    for i, word in enumerate(words):

        if word.isdigit():

            number = int(word)

            if i + 1 < len(words):

                unit = words[i + 1]

                if "second" in unit:
                    seconds = number

                elif "minute" in unit:
                    seconds = number * 60

                elif "hour" in unit:
                    seconds = number * 60 * 60

            break

    if seconds == 0:
        speak("Please tell me the reminder time.")
        return

    if " to " in command:

        message = command.split(" to ", 1)[1].strip()

    else:

        message = "Your reminder"

    set_reminder(seconds, message)

    speak("Reminder set for " + message)

# -----------------------------
# Send Email Command
# -----------------------------
# -----------------------------
# Clean Email Address
# -----------------------------

def clean_email_address(email):

    email = email.lower().strip()

    replacements = {
        " at gmail.com": "@gmail.com",
        " at gmail dot com": "@gmail.com",
        " at yahoo.com": "@yahoo.com",
        " at yahoo dot com": "@yahoo.com",
        " at outlook.com": "@outlook.com",
        " at outlook dot com": "@outlook.com",
        " at ": "@",
        " dot com": ".com"
    }

    for spoken, actual in replacements.items():
        email = email.replace(spoken, actual)

    email = email.replace(" ", "")

    return email
def email_command(source):

    speak("Who should I send the email to?")

    recipient = listen(source)

    if recipient:
        recipient = clean_email_address(recipient)

    if not recipient:
        speak("I could not understand the email address.")
        return

    speak("What is the subject?")

    subject = listen(source)

    if not subject:
        speak("I could not understand the subject.")
        return

    speak("What should I write in the email?")

    message = listen(source)

    if not message:
        speak("I could not understand the message.")
        return

    success = send_email(
        recipient,
        subject,
        message
    )

    if success:
        speak("Email sent successfully.")

    else:
        speak("Sorry, I could not send the email.")
# -----------------------------
# Process Commands
# -----------------------------

def process_command(command, source):

    intent = predict_intent(command)

    if intent == "greeting":

        speak("Hello! How can I help you?")


    elif intent == "get_time":

        current_time = datetime.now().strftime("%I:%M %p")

        speak(
            "The current time is "
            + current_time
        )


    elif intent == "get_date":

        current_date = datetime.now().strftime("%d %B %Y")

        speak(
            "Today's date is "
            + current_date
        )


    elif intent == "search":

        search_web(command)

    elif intent == "weather":
        weather_command(command, source)

    elif intent == "send_email":
        email_command(source)

    elif intent == "reminder":
        create_reminder(command)

    elif intent == "general_question":
        answer = answer_question(command)
        speak(answer)
        
    elif intent == "custom_command":
        response = execute_custom_command(command)
        speak(response)

    elif intent == "exit":

        speak("Goodbye!")

        return False


    else:

        speak(
            "Sorry, I don't understand that command yet."
        )


    return True


# -----------------------------
# Microphone
# -----------------------------

with sr.Microphone(device_index=1) as source:

    print("Adjusting for background noise...")

    recognizer.adjust_for_ambient_noise(
        source,
        duration=0.5
    )

    print("Voice assistant is ready!")


    # -----------------------------
    # Continuous Listening
    # -----------------------------

    while True:

        command = listen(source)

        if command:

            continue_running = process_command(command, source)

            if not continue_running:
                break