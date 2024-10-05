import numpy as np
import time
from pydub import AudioSegment
from pydub.playback import play
import multilineMAX7219 as LEDMatrix

# Initialize the library and the MAX7219/32x24LED arrays
LEDMatrix.init()

# Set up the audio recording parameters
duration = 0.1  # seconds
sample_rate = 44100

# Load the audio file
audio_path = "MP3/sample.mp3"
audio = AudioSegment.from_file(audio_path)

# Start playing the music
play(audio)

try:
    while play(audio).is_playing():  # Continue the loop while the music is playing
        # Read a chunk of audio data
        audio_array = np.array(audio.raw_data, dtype=np.int16)

        # Calculate the RMS value of the audio chunk
        rms_value = np.sqrt(np.mean(audio_array**2))

        # Map the RMS value to a bar height (adjust as needed)
        bar_height = int(24 * rms_value / 32768)  # Assuming 16-bit audio

        # Update the bar height with some smoothing
        bar_height = max(bar_height * 0.9, bar_height)

        print(f"RMS Value: {rms_value}, Bar Height: {bar_height}")

        # Display the bar on the LED matrix
        for j in range(24):
            if j < bar_height:
                LEDMatrix.gfx_set_px(0, j, 1)  # Using only the first bar for simplicity
            else:
                LEDMatrix.gfx_set_px(0, j, 0)

        # Render the LED matrix
        LEDMatrix.gfx_render()

        # Add a small delay to control the loop speed
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass  # Allow the user to stop the program with Ctrl-C
finally:
    # Stop the music when the loop ends
    play(audio).stop()

    # Clean up
    LEDMatrix.cleanup()
