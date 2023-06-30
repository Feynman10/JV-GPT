import speech_recognition as sr
import openai
from gtts import gTTS
import os
import webbrowser

# Set up the speech recognizer
r = sr.Recognizer()

# Set up the OpenAI API key
openai.api_key = 'Your API'

# Set up the gTTS text-to-speech engine
tts_engine = gTTS

def get_command():
    with sr.Microphone() as source:
        print("Listening for keyword activation...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

def validate_command(command):
    valid_commands = ["open GitHub", "open Google"]  # Add your valid commands here

    for valid_command in valid_commands:
        if valid_command.lower() in command.lower():
            return True

    print("Invalid command. Please try again.")
    return False

def generate_response(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with the desired GPT-4 model name
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def speak(text):
    tts = tts_engine(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("afplay temp.mp3")

def execute_command(command):
    if command.lower() == "open GitHub":
        webbrowser.open("https://github.com")
    elif command.lower() == "open Google":
        webbrowser.open("https://www.google.com")
    # Add more commands here

def main():
    print("Welcome to the Assistant!")

    while True:
        print("\nListening for a command...")
        command = get_command()

        if not command:
            continue

        print(f"Command received: {command}")

        if command.lower() == "complete it":
            print("Ordering completed. Exiting...")
            break

        if not validate_command(command):
            continue

        print("Generating a response...")
        response = generate_response(command)

        print(f"Response: {response}")

        print("Speaking the response...")
        speak(response)

        print("Executing the command...")
        execute_command(command)

if __name__ == "__main__":
    main()
