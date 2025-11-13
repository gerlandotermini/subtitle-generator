#!/usr/bin/env python3

import argparse
import sys
import os
import shutil
import whisper
import torch


def format_time(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"


def check_ffmpeg():
    """Controlla se ffmpeg è disponibile nel PATH."""
    if shutil.which("ffmpeg") is None:
        print("Errore: 'ffmpeg' non è installato o non è nel PATH.")
        print("Su Ubuntu/Debian puoi installarlo con:")
        print("  sudo apt update && sudo apt install ffmpeg")
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Genera sottotitoli SRT da un file audio usando OpenAI Whisper."
    )
    parser.add_argument(
        "audio_file",
        help="Percorso del file audio o video (es. audio.wav, video.mp4)"
    )
    parser.add_argument(
        "-m", "--model",
        default="small",
        help="Modello Whisper da usare (tiny, base, small, medium, large). Default: small"
    )
    parser.add_argument(
        "-l", "--language",
        default="it",
        help="Codice lingua (es. it, en, fr). Default: it"
    )
    parser.add_argument(
        "-t", "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Task: 'transcribe' per trascrivere nella stessa lingua, 'translate' per tradurre in inglese. Default: transcribe"
    )
    parser.add_argument(
        "-o", "--output",
        help="Percorso file SRT di output. Se non specificato, usa lo stesso nome dell'audio con estensione .srt"
    )
    parser.add_argument(
        "--device",
        choices=["cpu", "cuda"],
        help="Forza il device: cpu o cuda. Default: auto"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostra output dettagliato di Whisper."
    )
    return parser.parse_args()


def choose_device(user_choice: str | None) -> str:
    if user_choice:
        return user_choice
    return "cuda" if torch.cuda.is_available() else "cpu"


def main():
    # Se l'utente non passa argomenti, mostra un messaggio utile
    if len(sys.argv) == 1:
        print("Uso: python3 genera_sottotitoli.py <file_audio> [opzioni]")
        print("Suggerimento: usa --help per vedere tutte le opzioni disponibili.\n")
        sys.exit(1)

    args = parse_args()

    # 1. Controllo ffmpeg
    check_ffmpeg()

    audio_path = args.audio_file

    # 2. Controllo file esistente
    if not os.path.exists(audio_path):
        print(f"Errore: file non trovato: {audio_path}")
        sys.exit(1)

    # 3. Determina il percorso del file SRT di output
    if args.output:
        srt_path = args.output
    else:
        srt_path = os.path.splitext(audio_path)[0] + ".srt"

    # 4. Scelta device
    device = choose_device(args.device)
    print(f"Uso il device: {device}")

    # 5. Carica modello
    print(f"Carico il modello Whisper: {args.model}")
    try:
        model = whisper.load_model(args.model, device=device)
    except Exception as e:
        print(f"Errore nel caricamento del modello '{args.model}': {e}")
        sys.exit(1)

    # 6. Parametri di transcribe
    use_fp16 = device == "cuda"

    print(f"Trascrivo: {audio_path}")
    print(f"Task: {args.task}, lingua: {args.language}, fp16: {use_fp16}")

    try:
        result = model.transcribe(
            audio_path,
            task=args.task,
            language=args.language,
            fp16=use_fp16,
            verbose=args.verbose
        )
    except KeyboardInterrupt:
        print("\nInterrotto dall'utente.")
        sys.exit(1)
    except Exception as e:
        print(f"Errore durante la trascrizione: {e}")
        sys.exit(1)

    segments = result.get("segments", [])
    if not segments:
        print("Nessun segmento trovato nella trascrizione.")
        sys.exit(1)

    # 7. Scrittura file SRT
    try:
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments, start=1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()

                srt_file.write(f"{i}\n")
                srt_file.write(f"{format_time(start)} --> {format_time(end)}\n")
                srt_file.write(f"{text}\n\n")

        print(f"Sottotitoli salvati in: {srt_path}")
    except Exception as e:
        print(f"Errore nella scrittura del file SRT: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
