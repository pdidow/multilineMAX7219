import time
import multilineMAX7219 as LEDMatrix
from pydub import AudioSegment
from pydub.playback import play

# Initialise the library and the MAX7219/32x24LED arrays
LEDMatrix.init()

# Load the audio file
audio = AudioSegment.from_file("MP3/sample.mp3")

# Start playing the music
play(audio)

# Define the number of bars and their initial heights
num_bars = 32
bar_heights = [0] * num_bars

# Game loop
running = True
try:
    while running:
        # Display a message to the console for each iteration
        print("Loop iteration")
        # Analyze the audio levels for each bar
        audio_levels = audio.get_array_of_samples()

        for i in range(num_bars):
            # Calculate the average audio level for the corresponding bar
            start_index = int(i * len(audio_levels) / num_bars)
            end_index = int((i + 1) * len(audio_levels) / num_bars)
            average_level = sum(audio_levels[start_index:end_index]) / (end_index - start_index)

            # Map the average audio level to a bar height (adjust as needed)
            bar_height = int((average_level + 32768) / 2000)

            # Update the bar height with some smoothing
            bar_heights[i] = max(bar_heights[i] * 0.9, bar_height)

            # Display the bar on the LED matrix
            for j in range(24):
                if j < bar_height:
                    LEDMatrix.gfx_set_px(i, j, 1)
                else:
                    LEDMatrix.gfx_set_px(i, j, 0)

        # Render the LED matrix
        LEDMatrix.gfx_render()
        # Diagnostic print statements
        print(f"i: {i}, j: {j}, bar_height: {bar_height}")

        # Add a small delay to control the loop speed
        time.sleep(0.1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass

# Stop the music when the loop ends
pygame.mixer.music.stop()

# Clean up
