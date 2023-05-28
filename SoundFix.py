import numpy as np
import soundfile as sf
import sounddevice as sd
from pydub import AudioSegment
from pydub.effects import flanger

# Funció que llegeix un fitxer d'àudio en .mp3 i el transforma a .wav
#fm = 10000
#fitxer_mp3, fm = sf.read("Summer_Wine.mp3")

def convert2wav(fitxer_mp3, fitxer_wav):
    """
    Agafa com a arguments fitxer_mp3, que es la ruta del fitxer mp3 que es
    desitja convertir i fitxer_wav, que es la ruta del fitxer wav de sortida.
    """
    audio = AudioSegment.from_mp3(fitxer_mp3)
    audio.export(fitxer_wav, format = "wav") # Es guarda l'àudio en format WAV especificant la ruta i el format desitjat
    #return fitxer_wav

# Rutas dels fitxers MP3 i WAV
fitxer_mp3 = "Summer_Wine.mp3"
x_r, fm = sf.read('Summer_Wine.mp3')
sf.write('Summer_Wine.wav', x_r, fm) 
fitxer_wav = "Summer_Wine.wav"

# Crida a la funció per convertir de MP3 a WAV
convert2wav(fitxer_mp3, fitxer_wav)

# Lectura del fitxer WAV convertit
audio, fm = sf.read(fitxer_wav)   

# Reproducció de l'audio
#sd.play(audio, fm)
#sd.wait()

def retallar_audio(fitxer_wav, output_file, inici, duracio):
    """
    Retalla el fitxer d'àudio WAV en segments personalitzats.

    Args:
        fitxer_wav (str): Ruta del fitxer d'àudio d'entrada en format WAV.
        output_file (str): Ruta del fitxer d'àudio de sortida en format WAV.
        inici (floa): Temps d'inici en segons del segment a retallar.
        duracio (float): Duració en segons del segment a retallar.
    """
    # Llegim el fitxer d'entrada
    audio, samplerate = sf.read(fitxer_wav)
    
    # Calcular els índexs corresponents al segment a retallar
    inici_mostra = int(inici * samplerate)
    final_mostra = int((inici + duracio) * samplerate)
    
    # Retallem el segment d'àudio
    segment = audio[inici_mostra:final_mostra]
    
    # Escribim el segment d'àudio en el fitxer de sortida
    sf.write(output_file, segment, samplerate)
    
# Exemple d'ús
output_file = "Segment.wav"
inici =  5.0
duracio = 20.0

retallar_audio(fitxer_wav, output_file, inici, duracio)

def efecto_robot(input_file, output_file):
    """
    Aplica un efecte de robot a un fitxer d'audio WAV

    """
    # Llegim el fitxer d'àudio d'entrada
    audio, samplerate = sf.read(input_file)
    
    # Apliquem l'efecte de robot
    factor = 0.8 #factor de modulació
    factor_pitch = 0.9
    modulacio = np.arange(0, len(audio)) * (1.0 / samplerate) * factor
    mod = np.sin(2 * np.pi * modulacio)
    audio_ajustat = audio * mod[:, np.newaxis]
    
    
    # Normalitzem els valors de l'àudio
    max_valor = np.max(np.abs(audio_ajustat))
    audio_modulat = audio_ajustat / max_valor
    
    audio_robot = np.arange(0, len(audio_modulat)) * factor_pitch
    
    sf.write(output_file, audio_robot, samplerate)
 
#input_file = "Segment.wav"   
#output_file = "Robot.wav"

#efecto_robot(input_file, output_file)


def efecte_eco(input_file, output_file, delay=0.7, decay=0.5):
    """
    Aplica un efecte eco a un fitxer d'àudio WAV
    
    Args:
        input_file(str): Ruta del fitxer d'entrada
        output_file(str): Ruta del fitxer de sortida
        delay (int): Temps de retràs en mil·lisegons per l'eco (per defecte: 1000ms)
        decay (float): Factor de decaiment de l'eco (per defecte: 0.5)
    """
    # Carreguem el fitxer d'àudio
    audio, samplerate = sf.read(input_file)
    
    delay_samples = int(delay * samplerate)

    # Creem un arreglo per l'àudio de sortida
    output_audio = np.zeros_like(audio)

    # Apliquem l'efecte d'eco
    for i in range(len(audio)):
        if i >= delay_samples:
            output_audio[i] = audio[i] + decay * output_audio[i - delay_samples]
        else:
            output_audio[i] = audio[i]

    # Guardem l'àudio modificat en un fitxer WAV
    sf.write(output_file, output_audio, samplerate)
