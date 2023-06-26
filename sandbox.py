# Imports
import os
import time
from playsound import playsound
import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment


def pronunciation_phase(language):
    """ Pronunciation phase.

        The function is called by the menu.
        Load the vocabulary.txt into a list called words.
        The prompt ask for a phrase and the procedure
        read and list every word. and compare it with the
        records listed in the language folder.
        Then assembled in order to play.

        In case of failure to play a word, the program
        activates a subroutine that asks for the word
        in the phrase and records new audio to store.
        Add the new word into vocabulary.txt.


    """
    pronunciation_folder = "pronunciation_" + language
    words = []
    with open('vocabulary.txt', 'r') as file:
        for line in file:
            words.append(line.strip())
    sentence = input("Enter a sentence: ")
    count = 0
    for word in sentence.split():
        count += 1
        parts = ['A','B']
        if word in words and os.path.isfile(os.path.join(pronunciation_folder, word + ".wav")):
            exec(parts[0] + f"{count}=''")
            if exec(parts[0] + f"{count}") is None:
                exec(parts[0] + f"{count}=AudioSegment.from_wav(os.path.join(pronunciation_folder, word + '.wav'))")
            else:
                exec(parts[0] + f"{count}+=AudioSegment.from_wav(os.path.join(pronunciation_folder, word + '.wav'))")
            # Pronounce the word
            exec(parts[0]+f"{count}.export('output.wav', format='wav')")
            playsound('output.wav')
        else:
            try:
                # Pronounce the unknown word using gTTS
                print('Low-Cost TTS failed, switching to gTTS...')
                message = gTTS(text=word, lang=language, slow=False)
                message.save("unknown.wav")
                playsound("unknown.wav")
            except:
                # If gTTS fails, switch to pyTTSx3
                print('gTTS failed, switching to pyTTSx3...')
                engine = pyttsx3.init()
                engine.setProperty('voice', language)
                engine.say(word)
                engine.runAndWait()


pronunciation_phase('es')
