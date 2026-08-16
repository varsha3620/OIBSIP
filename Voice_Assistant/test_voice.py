import pyttsx3
from datetime import datetime

engine = pyttsx3.init()

current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%d %B %Y")

print("Time:", current_time)
print("Date:", current_date)

engine.say("The current time is " + current_time)
engine.say("Today's date is " + current_date)

engine.runAndWait()