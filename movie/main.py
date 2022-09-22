
# 모듈 로딩 후 오디오 추출
import moviepy.editor as mp

# clip = mp.VideoFileClip("avante_en.mp4")
# clip.audio.write_audiofile("audio.wav",codec='pcm_s16le')
import speech_recognition as sr
from googletrans import Translator

from gtts import gTTS


# initialize the recognizer
r = sr.Recognizer()
translator = Translator()
# open the file
with sr.AudioFile("audio.wav") as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data, language = "en-US")
    print(text)
    result = translator.translate(text, dest="ko", src='en')
    print(f"I like burger. => {result.text}")
    eng_wav = gTTS(result.text, lang = 'ko')
    eng_wav.save('eng.wav')







