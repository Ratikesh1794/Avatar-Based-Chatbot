import os
import csv
import openai
import requests
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import datetime
import random
from twilio.rest import Client

from google.cloud import speech_v1p1beta1 as speech

openai.organization = "org-mHfK51GWNeZ5igQ8hAo8TGUi"
openai.api_key = "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"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"ChatBot/avatar-390004-ea6c57f9ae2b.json"

openai.Model.list()

medication_time = None 

# Initialize speech recognition and text-to-speech
recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()
engine.setProperty('rate', 200)

# Define chatbot messages and prompts
welcome_prompt = """Welcome to our Elderly Emotional Support Chatbot. I am here to provide a caring and empathetic presence..."""

emergency_keywords = ["emergency", "help", "danger"]
goodbye_keywords = ["goodbye", "bye", "farewell", "see you", "take care"]

# Exercise Reccomendation

yoga_exercises = [
    "Deep breathing exercise: Inhale deeply through your nose for a count of four, hold your breath for a count of four, and exhale slowly through your mouth for a count of six. Repeat this cycle several times.",
    "Mountain pose: Stand tall with your feet hip-width apart, spine elongated, shoulders relaxed, and arms hanging by your sides. Take slow and deep breaths, focusing on grounding your feet to the floor.",
    "Chair yoga: Sit comfortably on a chair with your feet flat on the floor. Gently rotate your neck clockwise and then counterclockwise. Lift your arms overhead and stretch upward. Repeat a few times.",
    "Seated forward bend: Sit on a chair with your feet flat on the floor. Slowly hinge forward from your hips, reaching towards your toes or shins. Hold the stretch for a few breaths and then slowly come back up.",
    "Legs-up-the-wall pose: Lie down on the floor near a wall and extend your legs vertically against the wall. Rest your arms by your sides and close your eyes. Relax and focus on deep breathing for a few minutes.",
    "Supported bridge pose: Lie on your back with your knees bent and feet flat on the floor. Place a yoga block or folded blanket under your hips for support. Gently lift your hips upward and hold for a few breaths.",
    "Corpse pose: Lie on your back, legs extended, and arms relaxed by your sides. Close your eyes and bring your attention to your breath. Allow your body to relax completely and let go of any tension.",
    "Seated cat-cow pose: Sit on a chair with your feet flat on the floor and hands resting on your thighs. Inhale as you arch your spine, lifting your chest and gazing upward (cow pose). Exhale as you round your spine, tucking your chin to your chest (cat pose). Repeat this flow for several rounds.",
    "Seated twist: Sit on a chair with your feet flat on the floor. Place your right hand on the outside of your left thigh and gently twist your torso to the left. Hold the twist for a few breaths and then switch sides.",
    "Supported tree pose: Stand next to a wall or use a chair for support. Shift your weight onto your left foot and place your right foot against your left inner thigh or calf. Find your balance and bring your hands to your heart center. Hold for a few breaths and then switch sides.",
    "Warrior II pose: Stand with your feet wide apart, facing forward. Turn your right foot out 90 degrees and bend your right knee, keeping it aligned with your ankle. Extend your arms out to the sides and gaze over your right fingertips. Hold for a few breaths and then switch sides.",
    "Chair pigeon pose: Sit on a chair with your feet flat on the floor. Cross your right ankle over your left thigh and gently press your right knee away from you. Keep your back straight and hold for a few breaths. Switch sides and repeat.",
    "Supported fish pose: Sit on the edge of a chair with your feet flat on the floor. Place your hands behind you, fingers pointing towards your hips. Lift your chest upward and lean back, allowing your head to gently drop back. Hold the stretch for a few breaths.",
    "Alternate nostril breathing: Sit comfortably with your back straight. Close your right nostril with your right thumb and inhale through your left nostril. Close your left nostril with your ring finger and exhale through your right nostril. Continue this pattern, alternating the nostrils with each breath.",
]

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Adjust the energy_threshold and silence_duration parameters
    recognizer.energy_threshold = 4000  # Adjust this value to set the minimum energy level for recording
    recognizer.pause_threshold = 0.5  # Adjust this value to set the minimum duration of silence to end a phrase

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        client = speech.SpeechClient()

        audio_data = audio.get_wav_data()
        audio = speech.RecognitionAudio(content=audio_data)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code='en-US'
        )

        response = client.recognize(config=config, audio=audio)

        if response.results:
            user_input = response.results[0].alternatives[0].transcript
            print("You said:", user_input)
            return user_input
        speak("Sorry, I couldn't understand.")
        print("Sorry, I couldn't understand.")
        return ""
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        speak("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't understand.")
        print("Sorry, there was an issue with the speech recognition service.")
        return ""
    

#speaking function
    
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate',200)
    engine.say(text)
    engine.runAndWait()
    
def get_user_personality(user_id):
    with open('user.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['User_ID'] == user_id:
                return {
                    'Extraverted': int(row['Extraverted']),
                    'Intutive': int(row['Intutive']),
                    'Assertive': int(row['Assertive']),
                    'Judging': int(row['Judging']),
                    'Feeling': int(row['Feeling'])
                }
    
    return None


def set_medication_reminder():
    speak("Please provide the time for medication reminder.")
    print("Please provide the time for medication reminder.")
    user_input = listen()
    try:
        medication_time = datetime.datetime.strptime(user_input, "%H:%M").time()
        print("Medication reminder set for:", medication_time)
        speak("Medication reminder set for " + user_input)
        return medication_time
    except ValueError:
        print("Invalid time format. Please try again.")
        speak("Invalid time format. Please try again.")
        return None
    

def check_medication_reminder(medication_time):
    if medication_time is None:
        return
    
    current_time = datetime.datetime.now().time()
    if current_time == medication_time:
        speak("It's time to take your medication.")
        print("Medication reminder:", current_time)
        

def suggest_yoga_exercise(user_message):
    if any(keyword in user_message.lower() for keyword in ["stress", "panic"]):
        exercise = random.choice(yoga_exercises)
        print("I suggest trying the following exercise to help you relax:\n", exercise)
        speak("I suggest trying the following exercise to help you relax:")
    

def contact_emergency_contacts():
    # Twilio account credentials
    account_sid = 'AC62b1f2c99e29660ec12bc542c23f4d14'
    auth_token = '9c4000014ebc65279003192ac4d79cf4'
    twilio_phone_number = '+14065057764'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Define your emergency contact phone numbers
    emergency_contacts = {
        'Contact 1': '+919731997690',
        'Contact 2': '+918603702284',
        # Add more contacts as needed
    }

    # Send SMS message to each emergency contact
    for name, phone_number in emergency_contacts.items():
        message = client.messages.create(
            body='Emergency! Please contact me immediately.',
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f'Sent emergency message to {name} at {phone_number}. Message SID: {message.sid}')

    # Make a phone call to each emergency contact (optional)
    for name, phone_number in emergency_contacts.items():
        call = client.calls.create(
            url='http://twimlets.com/message?Message%5B0%5D=Emergency%21%20Please%20contact%20me%20immediately.',
            from_=twilio_phone_number,
            to=phone_number
        )
        print(f'Made emergency call to {name} at {phone_number}. Call SID: {call.sid}')
        

def get_facial_expression():
    
    return None


def generate_empathetic_response(user_message, facial_expression, user_personality, max_tokens=200):
    prompt = f'User data: {user_message}, Facial Expression: {facial_expression}, User Personality: {user_personality}\n\n' \
             'Welcome to our Elderly Emotional Support Chatbot. I am here to provide a caring and empathetic presence...'
    
    payload = {
        'messages': [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': user_message}
        ]
    }
    
    response = openai.ChatCompletion.create(
        messages=payload['messages'],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.85,
        timeout=10,
        model="gpt-3.5-turbo",
    )

    chatbot_response = response.choices[0]['message']['content']
    
    words = chatbot_response.split()
    truncated_response = ' '.join(words[:max_tokens])
    
    return truncated_response

def main():
    speak("Hello, this is Buddy! How can I help you?")
    print("Hello, this is Buddy! How can I help you?")
    
    while True:
        user_input = listen()
        user_id = '111'  # Change this to the desired user ID
        user_facial_expression = get_facial_expression()
        user_personality = get_user_personality(user_id)
        
        if user_personality:
            print(f"User {user_id}'s personality traits:", user_personality)
        else:
            print(f"User {user_id} not found in the personality data.")  # Assuming you have a function for this
            user_personality = get_user_personality()  # Assuming you have a function for this
        
        response = generate_empathetic_response(user_input, user_facial_expression, user_personality)
        print(response)
        speak(response)
        
        # ... Rest of the code ...

if __name__ == "__main__":
    main()



def main():
    speak("Hello, this is Buddy! How can I help you?")
    print("Hello, this is Buddy! How can I help you?")
    
    while True:
        user_input = listen()
        
        user_facial_expression = get_facial_expression() 
        
        user_id = '111'
        user_personality = get_user_personality(user_id)
        if user_personality:
            print(f"User {user_id}'s personality traits:", user_personality)
        else:
            print(f"User {user_id} not found in the personality data.") 
        
        
        response = generate_empathetic_response(user_input)
        print(response)
        speak(response)
        
        if any(keyword in user_input.lower() for keyword in emergency_keywords):
            contact_emergency_contacts()
        
        if any(keyword in user_input.lower() for keyword in ["reminder", "medication"]):
            if medication_time is None:
                medication_time = set_medication_reminder()
        
        suggest_yoga_exercise(user_input)
        
        check_medication_reminder(medication_time)
        
        if any(keyword in user_input.lower() for keyword in goodbye_keywords):
            print("Goodbye! Take care.")
            speak("Goodbye! Take care.")
            exit(0)


if __name__ == "__main__":
    main()
