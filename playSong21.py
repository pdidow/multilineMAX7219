import os
import time
import pygame
import numpy as np
import multilineMAX7219 as LEDMatrix

# Initialize the library and the MAX7219/32x24LED arrays
LEDMatrix.init()

# Set up the audio recording parameters
duration = 0.1  # seconds
sample_rate = 44100

# Specify the relative path to the MP3 file
relative_path = "MP3/sample.mp3"

# Get the absolute path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full file path
audio_path = os.path.join(script_dir, relative_path)

# Print the full file path for debugging
print(f"Full File Path: {audio_path}")

# Try initializing Pygame and loading the audio file
try:
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    print("Pygame and Audio Loaded Successfully")
except pygame.error as e:
    print(f"Error during Pygame or Audio initialization: {e}")

# Rest of the script...
try:
    while pygame.mixer.music.get_busy():  # Continue the loop while the music is playing
        # Get the playback position in milliseconds
        pos_ms = pygame.mixer.music.get_pos()

        # Play the Sound object to get the raw audio data
        sound.play()
        pygame.time.delay(100)  # Delay to allow time for sound playback

        # Stop the Sound object
        sound.stop()

        # Get the raw audio data
        raw_audio = pygame.sndarray.array(sound)

        # Convert the raw audio data to a numpy array
        audio_array = np.frombuffer(raw_audio, dtype=np.int16)

        # Calculate the RMS value of the audio chunk
        rms_value = np.sqrt(np.mean(audio_array**2))

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
        print(f"Position: {pos_ms} ms, RMS Value: {rms_value}, Bar Height: {bar_height}")

        # Add a small delay to control the loop speed
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass  # Allow the user to stop the program with Ctrl-C
finally:
    # Stop the music when the loop ends
    pygame.mixer.music.stop()

    # Clean up
    #LEDMatrix.cleanup()
