import speech_recognition as sr

def speechRecognition():
    r = sr.Recognizer()
    result = ''
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
    except sr.UnknownValueError:
        result = "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        result = "Could not request results from Google Speech Recognition service; {0}".format(e)

    return result