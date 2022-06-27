import speech_recognition

# The Recognizer is initialized.
UserVoiceRecognizer = speech_recognition.Recognizer()

def recorgniseAudio():
    while(1):
        try:
            with speech_recognition.Microphone() as UserVoiceInputSource:
                UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)
                UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)
                UserVoiceInput_converted_to_Text = UserVoiceRecognizer.recognize_google(UserVoiceInput)
                UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()
                print(UserVoiceInput_converted_to_Text)
        
        except KeyboardInterrupt:
            print('Terminating the Program due to keyboard interrupt!!!')
            exit(0)
        
        except speech_recognition.UnknownValueError:
            print("No User Voice detected OR unintelligible noises detected OR the recognized audio cannot be matched to text \n Please try again!!!")