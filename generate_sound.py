import numpy as np
import wave
import pygame

def generate_tone_file(filename, duration, frequency, sample_rate=44100, amplitude=32767):
    """
    Generate a tone and save it as a WAV file.

    Parameters:
    filename (str): The name of the file to save.
    duration (float): The duration of the tone in seconds.
    frequency (float): The frequency of the tone in Hz.
    sample_rate (int): The sample rate in samples per second.
    amplitude (int): The amplitude of the tone.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    waveform = waveform.astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16 bits per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(waveform.tobytes())

generate_tone_file('dot.wav', 0.2, 800)
generate_tone_file('dash.wav', 0.6, 800)

# Initialize pygame mixer
pygame.mixer.init()
