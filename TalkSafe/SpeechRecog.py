from speech_recognition import Microphone, Recognizer, AudioFile, WaitTimeoutError, UnknownValueError


def recognize():
    rec = Recognizer()
    mic = Microphone()
    try:
        with mic:
            audio = rec.listen(mic, 5)
            recognized = rec.recognize_google(audio)
            word = "You said: " + str(recognized)

            return str(recognized)
    except WaitTimeoutError:
        error = "No word/s recognized, Try again."
        return error
    except UnknownValueError:
        error = "Please try again."
        return error


def continuous_recognize():
    rec = Recognizer()
    mic = Microphone()
    try:
        with mic:
            audio = rec.listen(mic)
            recognized = rec.recognize_google(audio)
            word = "You said: " + str(recognized)

            return str(recognized)
    except WaitTimeoutError:
        error = "No word/s recognized, Try again."
        return error
    except UnknownValueError:
        error = "Please try again."
        return error

