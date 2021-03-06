import speech_recognition as sr
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from operator import itemgetter
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pyttsx3
import random
# "googleAPI.py" imports
from googleAPI import getCalendars, getEvents, searchEmails, serviceCalendar, serviceGmail


stop_words = set(stopwords.words("english"))
engine = pyttsx3.init()
lemmatizer = WordNetLemmatizer()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[35].id)
# n=0
# for voice in engine.getProperty('voices'):
#     print(n)
#     print(voice)
#     n+=1

# The Recognizer is initialized.
voice_recognizer = sr.Recognizer()
greetings = [
    "What's up ?",
    "Hello",
    "Hi there",
    "Hey how may I assist you ?",
    "How may I help you today",
]
keywords_identifier = {
    'ListCalendars': [
        "show calendar",
        "please show calendar",
        "list all my calendar",
        "show calendar",
        "display calendar",
        "list calendar",
        "calendar list",
        "give calendar",
        "name calendar",
        "calendar",
        "my calendar"
    ],
    'ListEvents':[
        "show event",
        "please show event",
        "list all my event",
        "show all event",
        "list event",
        "event list",
        "give calendar",
        "name calendar",
        "my event",
        "event",
        "upcoming event",
        "event upcoming"
    ],
    'SearchEmails':[
        "search email",
        "email search",
        "show email",
        "display email",
        "email"
    ]
}

def fetchKey(filtered_sentence):
    key = ""
    for i, j in keywords_identifier.items():
        for k in j:
            if filtered_sentence in j:
                key = i
                break
    return key


def nlpConvert(user_input):
    word_tokens = word_tokenize(user_input)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            w = lemmatizer.lemmatize(w)
            filtered_sentence.append(w)
    filtered_sentence = str(' '.join(filtered_sentence))
    filtered_sentence = ' '.join(dict.fromkeys(filtered_sentence.split()))
    key = fetchKey(filtered_sentence)
    return key


# Listen to audio
def recorgniseAudio():
    print("Say something...")
    while(1):
        engine.say(random.choice(greetings))
        engine.runAndWait()
        try:
            with sr.Microphone() as input_device:
                voice_recognizer.adjust_for_ambient_noise(input_device, duration=0.5)
                voice_input = voice_recognizer.listen(input_device)
                voice_to_text = voice_recognizer.recognize_google(voice_input)
                voice_to_text = voice_to_text.lower()
                engine.say("Inputted message is: "+ voice_to_text)
                engine.runAndWait()
                print("Original message: "+ voice_to_text)    
                result = nlpConvert(voice_to_text)
                if result == "ListCalendars":
                    calendars = getCalendars(serviceCalendar)
                    print("Calendars", calendars)
                    engine.say("I found "+str(len(calendars))+"calendars in your list")
                    engine.runAndWait()
                    engine.say("Your calendars are "+' '.join(calendars))
                    engine.runAndWait()
                elif result == "ListEvents":
                    events = getEvents(serviceCalendar)
                    print("Events", events)
                    engine.say("I found "+str(len(events))+"events in your list")
                    engine.runAndWait()
                    engine.say("Your events are "+' '.join(events))
                    engine.runAndWait()
                elif result == "SearchEmails":
                    resultMail, resultSubject = searchEmails(serviceGmail, ['INBOX'], 'from:PlayStation')
                    engine.say("I found "+str(len(resultMail))+" in your inbox")
                    engine.runAndWait()
                    for i in range(len(resultSubject)):
                        engine.say("Subject "+str(i+1)+str(resultSubject[i]))
                        engine.runAndWait()
                else:
                    engine.say("Your input doesn't match any criteria would you mind reframing your query and sayning that again")
                    engine.runAndWait()
                break
        except KeyboardInterrupt:
            print('Terminating the Program due to keyboard interrupt!!!')
            engine.say("Terminating the Program due to keyboard interrupt!!!")
            engine.runAndWait()
            exit(0)       
        except sr.UnknownValueError as e:
            print(str(e))
            engine.say("Didn't get you, would you mind saying that again..")
            engine.runAndWait()

recorgniseAudio()

