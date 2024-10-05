import time
import pygame
import numpy as np
import multilineMAX7219 as LEDMatrix

# Initialize the library and the MAX7219/32x24LED arrays
LEDMatrix.init()

# Set up the audio recording parameters
duration = 0.1  # seconds
sample_rate = 44100

# Load the audio file
audio_path = "MP3/sample.mp3"
pygame.mixer.init()
pygame.mixer.music.load(audio_path)

# Start playing the music
pygame.mixer.music.play()

try:
    while pygame.mixer.music.get_busy():  # Continue the loop while the music is playing
        # Dummy audio data for testing
        data = pygame.mixer.music.get_pos()
        # Calculate the RMS value of the audio chunk (this is a placeholder, replace it with actual audio processing)
        rms_value = data / 1000.0  # Use the position in milliseconds as a placeholder

        # Map the RMS value to a bar height (adjust as needed)
        bar_height = int(24 * rms_value / 32768)  # Assuming 16-bit audio

        # Update the bar height with some smoothing
        bar_height = max(bar_height * 0.9, bar_height)

        # Display the bar on the LED matrix
        for j in range(24):
            if j < bar_height:
                LEDMatrix.gfx_set_px(0, j, 1)  # Using only the first bar for simplicity
            else:
                LEDMatrix.gfx_set_px(0, j, 0)

        # Render the LED matrix
        LEDMatrix.gfx_render()

        # Print RMS value and bar height to the console
        print(f"RMS Value: {rms_value}, Bar Height: {bar_height}")

        # Add a small delay to control the loop speed
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass  # Allow the user to stop the program with Ctrl-C
finally:
    # Stop the music when the loop ends
    pygame.mixer.music.stop()
