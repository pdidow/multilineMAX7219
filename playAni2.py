#!/usr/bin/env python
import time
import os
import sys
import pyaudio
import wave
from multilineMAX7219 import GFX_OFF
import multilineMAX7219 as LEDMatrix

def read_sprite_files(folder_name):
    sprites = []
    for filename in os.listdir(folder_name):
        if filename.startswith("sprite_") and filename.endswith(".txt"):
            file_path = os.path.join(folder_name, filename)
            with open(file_path, "r") as file:
                try:
                    content_str = file.read().replace('[', '').replace(']', '').replace(',', ' ')
                    rows = content_str.split('\n')
                    content = [[int(num) for num in row.split()] for row in rows if row]
                    # Reverse each sprite vertically
                    reversed_sprite = list(reversed(content))
                    sprites.append(reversed_sprite)
                except ValueError as e:
                    print(f"Error reading file {filename}: {e}")
    return sprites

def play_first_audio(folder_name):
    for filename in os.listdir(folder_name):
        if filename.lower().endswith(('.mp3', '.wav')):
            audio_file = os.path.join(folder_name, filename)
            play_audio(audio_file)
            return  # Exit after playing the first audio file

def play_audio(file_path):
    chunk = 1024
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

if len(sys.argv) != 2:
    print("Usage: python devilDance.py <folder_name>")
    sys.exit(1)

folder_name = sys.argv[1]

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()

# Define animation frames by reading sprite files
animation_frames = read_sprite_files(folder_name)
# flip horizontal
animation_frames = list(reversed(animation_frames))

try:
    # Display animation and play the first song forever
    for i, frame in enumerate(animation_frames):
        LEDMatrix.gfx_set_all(GFX_OFF)
        LEDMatrix.gfx_sprite_array(frame, 0, 0)
        LEDMatrix.gfx_render()
        time.sleep(0.1)

        # Play the first song when the animation reaches its last frame
        if i == len(animation_frames) - 1:
            play_first_audio(folder_name)

except KeyboardInterrupt:
    # Reset array
    LEDMatrix.scroll_message_horiz(["", "Goodbye!", ""], 1, 8)
    LEDMatrix.clear_all()
