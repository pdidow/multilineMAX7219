import time
import multilineMAX7219 as LEDMatrix
from pydub import AudioSegment
import pygame.mixer

# Initialize the library and the MAX7219/32x24LED arrays
LEDMatrix.init()

# Initialize Pygame Mixer for audio
pygame.mixer.init(frequency=44100)

# Load the audio file
audio = AudioSegment.from_file("Wav/ImperialMarch60.wav")

# Start playing the music
pygame.mixer.music.load("Wav/ImperialMarch60.wav")
pygame.mixer.music.play()

# Define the number of bars and their initial heights
num_bars = 24
bar_heights = [0] * num_bars

# Define the window size for calculating average audio level
window_size = len(audio) // num_bars

# Game loop
try:
    while pygame.mixer.music.get_busy():
        # Analyze the audio levels for each bar using a sliding window
        for i in range(num_bars):
            start_index = i * window_size
            end_index = (i + 1) * window_size
            audio_chunk = audio[start_index:end_index]
            average_level = audio_chunk.rms  # Root Mean Square (RMS) value as the average audio level

            # Map the average audio level to a bar height (adjust as needed)
            bar_height = int(24 * average_level / 32768)  # Assuming 16-bit audio

            # Update the bar height with some smoothing
            bar_heights[i] = max(bar_heights[i] * 0.9, bar_height)

            # Display the bar on the LED matrix
            for j in range(24):
                if j < bar_heights[i]:
                    LEDMatrix.gfx_set_px(i, j, 1)
                else:
                    LEDMatrix.gfx_set_px(i, j, 0)

        # Render the LED matrix
        LEDMatrix.gfx_render()

        # Add a small delay to control the loop speed
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass  # Allow the user to stop the program with Ctrl-C

# Stop the music when the loop ends
pygame.mixer.music.stop()

# Clean up
LEDMatrix.cleanup()
pygame.mixer.quit()
