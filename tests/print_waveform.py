# print_waveform.py
# to run: poetry run python tests/print_waveform.py outputs/{name}.wav tests/{name}.png


import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_waveform(audio_path: str, output_path: str = "waveform.png"):
    y, sr = librosa.load(audio_path)
    duration = librosa.get_duration(y=y, sr=sr)

    # Time vector for x-axis
    time = np.linspace(0, duration, num=len(y))

    # Plot
    plt.figure(figsize=(14, 5))
    plt.plot(time, y, color='deeppink')
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Set x-axis tick interval (e.g. every 10 seconds)
    interval = 10  # Change this as needed
    xticks = np.arange(0, duration, interval)
    plt.xticks(xticks)

    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Waveform saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: poetry run python waveform_plot.py <audio_file_path> [output_image_path]")
    else:
        audio_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "waveform.png"
        plot_waveform(audio_path, output_path)
