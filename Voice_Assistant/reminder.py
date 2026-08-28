import time
import threading
import pyttsx3


def set_reminder(seconds, message):

    def reminder():

        time.sleep(seconds)

        print("\n🔔 Reminder:", message)

        engine = pyttsx3.init()
        engine.say("Reminder: " + message)
        engine.runAndWait()
        engine.stop()

    reminder_thread = threading.Thread(
        target=reminder,
        daemon=True
    )

    reminder_thread.start()