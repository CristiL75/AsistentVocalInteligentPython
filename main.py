from neuralintents import BasicAssistant
import speech_recognition
import pyttsx3 as tts
import sys  # Use this to exit the program if needed

# Setting up speech recognition
recognizer = speech_recognition.Recognizer()

# Initializing text-to-speech engine
speaker = tts.init()
speaker.setProperty('rate', 150)  # Set the voice speed of the robot

todo_list = ['Shopping', 'Clean the room', 'Do homework']

def add_note():
    global recognizer

    speaker.say("What do you want to write in the note?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a name for the note!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
            with open(filename, "w") as f:
                f.write(note)
                done = True
                speaker.say(f"Successfully created note {filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I didn't understand what you said!")

def add_todo():
    global recognizer
    speaker.say("What event do you want to add?")
    speaker.runAndWait()

    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)

                done = True

                speaker.say(f"Mission accomplished! Added {item} to the list")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I didn't understand")
            speaker.runAndWait()

def show_todo():
    speaker.say("Here's what you have to do today!")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def greetings():
    speaker.say("Hello, how can I help you?")
    speaker.runAndWait()

def goodbye():
    speaker.say("Goodbye")
    speaker.runAndWait()
    sys.exit(0)

# Mapping commands to functions
mappings = {
    "greetings": greetings,
    "add_todo": add_todo,
    "add_note": add_note,
    "show_todo": show_todo,
    "goodbye": goodbye
}

# Creating an instance of BasicAssistant
assistant = BasicAssistant('intents.json', method_mappings=mappings)
assistant.fit_model(epochs=50)
assistant.save_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
        assistant.process_input(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
