import numpy as np
import soundfile as sf
import sounddevice as sd
from pydub import AudioSegment

# Funció qie llegeix un fitxer d'àudio en .mp3 i el transforma a .wav
def convert2wav(fitxer_mp3, fitxer_wav):
    """
    Agafa com a arguments fitxer_mp3, que es la ruta del fitxer mp3 que es
    desitja convertir i fitxer_wav, que es la ruta del fitxer wav de sortida.
    """
    audio = AudioSegment.from_mp3(fitxer_mp3)
    audio.export(fitxer_wav, format = "wav") # Es guarda l'àudio en format WAV especificant la ruta i el format desitjat
    
