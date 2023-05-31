import numpy as np
import soundfile as sf
import sounddevice as sd
from pydub import AudioSegment
import pyrubberband
import librosa
import subprocess
import ffmpeg
from pydub.playback import play

class AudioProcessor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.audio, self.samplerate = sf.read(input_file)

    def save_audio(self, output_file):
        sf.write(output_file, self.audio, self.samplerate)

    def play_audio(self):
        sd.play(self.audio, self.samplerate)

    def stop_audio(self):
        sd.stop(self.audio)
    
    def trim_audio(self, output_file, start_time, duration):
        start_sample = int(start_time * self.samplerate)
        end_sample = int((start_time + duration) * self.samplerate)
        trimmed_audio = self.audio[start_sample:end_sample]
        sf.write(output_file, trimmed_audio, self.samplerate)


class RobotEffect(AudioProcessor):
    def apply_robot_effect(self, output_file, modulation_factor=0.1, pitch_factor=0.9):
        num_channels = self.audio.shape[1]  # Obtenir el número de canals
        mod = np.sin(2 * np.pi * np.arange(0, len(self.audio)) * (1.0 / self.samplerate) * modulation_factor)

        for channel in range(num_channels):
            audio_1d = self.audio[:, channel]  # Obtenir el canal actual com una millora unidimensional
            
            mod_channel = mod[:len(audio_1d)]  # Ajustar el tamañ de mod al tamañ del canal actual

            # Calcular els índexs de mostreig modulats
            indices = np.arange(len(audio_1d)) + mod_channel * self.samplerate * pitch_factor

            # Aplicar interpolació lineal per obtenir els valors d'àudio modulats
            modulated_audio = np.interp(indices, np.arange(len(audio_1d)), audio_1d)

            # Normalitzar l'àudio modulat
            max_value = np.max(np.abs(modulated_audio))
            modulated_audio /= max_value

            # Assignar l'àudio modulat al canal actual
            self.audio[:, channel] = modulated_audio

        # Guardar l'àudio modulat en el fitxer de sortida
        sf.write(output_file, self.audio, self.samplerate)


class EchoEffect(AudioProcessor):
    def apply_echo_effect(self, output_file, delay=0.7, decay=0.5):
        delay_samples = int(delay * self.samplerate)
        output_audio = np.zeros_like(self.audio)
        for i in range(len(self.audio)):
            if i >= delay_samples:
                output_audio[i] = self.audio[i] + decay * output_audio[i - delay_samples]
            else:
                output_audio[i] = self.audio[i]
        sf.write(output_file, output_audio, self.samplerate)
        
class FlangerEffect(AudioProcessor):
    def apply_flanger_effect(self, output_file, delay=0.003, depth=0.002, rate=0.2):
        delay_samples = int(delay * self.samplerate)
        depth_samples = int(depth * self.samplerate)
        modulator = depth_samples * np.sin(2 * np.pi * rate * np.arange(len(self.audio)) / self.samplerate)
        flanger_audio = np.zeros_like(self.audio)
        for i in range(len(self.audio)):
            if i >= delay_samples:
                index = int(i - delay_samples + modulator[i])
                flanger_audio[i] = self.audio[i] + self.audio[index]
            else:
                flanger_audio[i] = self.audio[i]
        sf.write(output_file, flanger_audio, self.samplerate)

class PitufoEffect(AudioProcessor):
    def apply_pitufo_effect(self, output_file, modulation_factor=0.1, pitch_factor=0.9):
        num_channels = self.audio.shape[1]
        mod = (2 * np.pi * np.arange(0, len(self.audio)) * (1.0 / self.samplerate) * modulation_factor)

        for channel in range(num_channels):
            audio_1d = self.audio[:, channel]    
            mod_channel = mod[:len(audio_1d)]  
            indices = np.arange(len(audio_1d)) + mod_channel * self.samplerate * pitch_factor
            modulated_audio = np.interp(indices, np.arange(len(audio_1d)), audio_1d)
            max_value = np.max(np.abs(modulated_audio))
            modulated_audio /= max_value
            self.audio[:, channel] = modulated_audio
        sf.write(output_file, self.audio, self.samplerate)

class LowEffect(AudioProcessor):
    def apply_low_effect(self, output_file, modulation_factor=0.1, pitch_factor=0.9):
        num_channels = self.audio.shape[1]
        mod = -(2 * np.pi * np.arange(0, len(self.audio)) * (1.0 / self.samplerate) * modulation_factor)

        for channel in range(num_channels):
            audio_1d = self.audio[:, channel]    
            mod_channel = mod[:len(audio_1d)]  
            indices = np.arange(len(audio_1d)) + mod_channel * self.samplerate * pitch_factor
            modulated_audio = np.interp(indices, np.arange(len(audio_1d)), audio_1d)
            max_value = np.max(np.abs(modulated_audio))
            modulated_audio /= max_value
            self.audio[:, channel] = modulated_audio
        sf.write(output_file, self.audio, self.samplerate)

class LowPassFilter(AudioProcessor):        
    def apply_lowpass_filter(self, output_file, cutoff_frequency=1800):
        audio = AudioSegment.from_file(self.input_file)
        filtered_audio = audio.low_pass_filter(cutoff_frequency)
        filtered_audio.export(output_file, format='wav')

class HighPassFilter(AudioProcessor):
    def apply_highpass_filter(self, output_file, cutoff_frequency=1800):
        audio = AudioSegment.from_file(self.input_file)
        filtered_audio = audio.high_pass_filter(cutoff_frequency)
        filtered_audio.export(output_file, format="wav")
