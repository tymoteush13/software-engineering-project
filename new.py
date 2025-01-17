import soundcard as sc
import soundfile as sf
import numpy as np
import threading
import keyboard

SAMPLE_RATE = 48000  # [Hz]. sampling rate.
stop_recording = False  # Flag to stop recording

def record_system_audio():
    global stop_recording
    OUTPUT_FILE_NAME = "out_system.wav"
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        print("Recording system audio... Press 's' to stop.")
        data = []
        while not stop_recording:
            frames = mic.record(numframes=SAMPLE_RATE)  # Record one second of audio
            data.append(frames[:, 0])  # Only keep the first channel
        print("System audio recording stopped.")
        data = np.concatenate(data, axis=0)  # Combine recorded chunks into one array
        sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)

def record_microphone_audio():
    global stop_recording
    OUTPUT_FILE_NAME = "out_mikro.wav"
    microphone = sc.default_microphone()
    with microphone.recorder(samplerate=SAMPLE_RATE) as mic:
        print("Recording microphone audio... Press 's' to stop.")
        data = []
        while not stop_recording:
            frames = mic.record(numframes=SAMPLE_RATE)  # Record one second of audio
            data.append(frames[:, 0])  # Only keep the first channel
        print("Microphone audio recording stopped.")
        data = np.concatenate(data, axis=0)  # Combine recorded chunks into one array
        sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)

def stop_recording_key():
    global stop_recording
    print("Press 's' to stop recording.")
    keyboard.wait('s')  # Wait for the 's' key to be pressed
    stop_recording = True

def merge_wav_files(system_file, microphone_file, output_file):
    data1, samplerate1 = sf.read(system_file)
    data2, samplerate2 = sf.read(microphone_file)
    
    # Ensure both files have the same sample rate
    if samplerate1 != samplerate2:
        raise ValueError("Sample rates do not match.")
    
    # Ensure both files have the same length
    min_length = min(len(data1), len(data2))
    data1 = data1[:min_length]
    data2 = data2[:min_length]
    
    # Average the audio data to create a mono track
    merged_data = (data1 + data2) / 2
    
    # Write the merged audio to output file
    sf.write(output_file, merged_data, samplerate1)
    print("Merged file created:", output_file)

# Create threads for simultaneous recording
system_thread = threading.Thread(target=record_system_audio)
microphone_thread = threading.Thread(target=record_microphone_audio)
stop_thread = threading.Thread(target=stop_recording_key)

# Start threads
system_thread.start()
microphone_thread.start()
stop_thread.start()

# Wait for threads to finish
system_thread.join()
microphone_thread.join()
stop_thread.join()

print("Recording completed.")

# Merge the recorded files
merge_wav_files("out_system.wav", "out_mikro.wav", "out_merged.wav")