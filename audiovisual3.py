import time
from threading import Thread
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play

# ... (rest of the code remains the same)

def playing_audio(wavFile, position):
    song = AudioSegment.from_wav(wavFile)
    play(song[position:])

def showing_audiotrack(wavFile, sound_axis, n, position):
    # We use a variable previousTime to store the time when a print update is made
    # and to then compute the time taken to update the progress of the audio data.
    previousTime = time.time()

    # Each time we go through a number of samples in the audio data that corresponds to one second of audio,
    # we increase spentTime by one (1 second).
    spentTime = 0

    # Let's define the update periodicity
    updatePeriodicity = 2  # expressed in seconds

    # Printing the progress information
    for i in range(position, n):
        # Each time we read one second of audio data, we increase spentTime:
        if i // Fs != (i - 1) // Fs:
            spentTime += 1
        # We update the progress every updatePeriodicity seconds
        if spentTime == updatePeriodicity:
            # Print the progress information to the console
            print(f"Position: {i}, RMS Value: {sound_axis[i]}", flush=True)
            time.sleep(updatePeriodicity - (time.time() - previousTime))
            # a forced pause to synchronize the audio being played with the audio track being displayed
            previousTime = time.time()
            spentTime = 0

if __name__ == "__main__":
    wavFile = "source_file.wav"
    data, samplerate = sf.read(wavFile)
    n = len(data)
    Fs = samplerate

    # Let's say you want to start graphing from 10 seconds into the song
    start_position = int(10 * Fs)

    # Define sound_axis based on the channel you want to analyze
    sound_axis = np.array([data[i][0] for i in range(n)])

    p1 = Thread(target=playing_audio, args=(wavFile, start_position))
    p1.start()
    p2 = Thread(target=showing_audiotrack, args=(wavFile, sound_axis, n, start_position))
    p2.start()
    p1.join()
    p2.join()
