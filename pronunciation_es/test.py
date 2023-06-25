"""from pydub import AudioSegment

sound1 = AudioSegment.from_wav("temprana.wav")
sound2 = AudioSegment.from_wav("sentir.wav")

combined_sounds = sound1 + sound2
combined_sounds.export("concatenate.wav", format="wav")"""

from pydub import AudioSegment
file_names = ["temprana.wav", "sentir.wav"]
sounds = [AudioSegment.from_wav(file_name) for file_name in file_names]
combined_sounds = sounds[0]
for sound in sounds[1:]:
    combined_sounds += sound
combined_sounds.export("concatenate.wav", format="wav")
