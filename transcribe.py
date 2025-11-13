#!/usr/bin/python3

import speech_recognition as sr
from pydub import AudioSegment
import sys
import os
import math
import tempfile

# Verifica argomento
if len(sys.argv) < 2:
    print("Uso: trascrivi_spezzato.py <nome_file_audio>")
    sys.exit(1)

audio_file = sys.argv[1]

# Costruisci nome file di output
output_file = os.path.splitext(audio_file)[0] + ".txt"

# Crea Recognizer
recognizer = sr.Recognizer()

try:
    # Carica file audio con pydub
    audio = AudioSegment.from_file(audio_file)
    duration_ms = len(audio)
    print(f"Durata audio: {duration_ms/1000:.2f} secondi")

    # Durata di ogni segmento in millisecondi
    chunk_duration_ms = 30000  # 30 secondi
    total_chunks = math.ceil(duration_ms / chunk_duration_ms)

    full_text = ""

    # Crea cartella temporanea per i segmenti
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i in range(total_chunks):
            start_ms = i * chunk_duration_ms
            end_ms = min((i+1) * chunk_duration_ms, duration_ms)

            chunk = audio[start_ms:end_ms]
            chunk_path = os.path.join(tmpdirname, f"chunk_{i}.wav")
            chunk.export(chunk_path, format="wav")

            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)

            try:
                result = recognizer.recognize_google(audio_data, language="it-IT")
                print(f"Segmento {i+1}: {result}")
                full_text += result + "\n"
            except sr.UnknownValueError:
                print(f"Segmento {i+1}: parlato non riconosciuto.")
                full_text += "[Parlato non riconosciuto]\n"
            except sr.RequestError as e:
                print(f"Errore di richiesta: {e}")
                full_text += f"[Errore di richiesta: {e}]\n"
                break

    # Salva il testo su file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text.strip())

    print(f"\n--- TRASCRIZIONE COMPLETA SALVATA IN: {output_file} ---")

except FileNotFoundError:
    print(f"Errore: Il file '{audio_file}' non esiste.")
except Exception as e:
    print(f"Errore durante l'elaborazione dell'audio: {e}")
