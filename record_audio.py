import soundcard as sc
import soundfile as sf
import numpy as np
import threading

SAMPLE_RATE = 48000  # [Hz]. sampling rate.
stop_recording = threading.Event()  # Use Event to signal stopping

def record_system_audio():
    OUTPUT_FILE_NAME = "out_system.wav"
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        print("Recording system audio...")
        data = []
        while not stop_recording.is_set():
            frames = mic.record(numframes=SAMPLE_RATE) # Record one second of audio
            data.append(frames[:, 0])  # Only keep the first channel
        print("System audio recording stopped.")
        data = np.concatenate(data, axis=0)  # Combine recorded chunks into one array
        sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)

def record_microphone_audio():
    OUTPUT_FILE_NAME = "out_mikro.wav"
    microphone = sc.default_microphone()
    with microphone.recorder(samplerate=SAMPLE_RATE) as mic:
        print("Recording microphone audio...")
        data = []
        while not stop_recording.is_set():
            frames = mic.record(numframes=SAMPLE_RATE) # Record one second of audio
            data.append(frames[:, 0])  # Only keep the first channel
        print("Microphone audio recording stopped.")
        data = np.concatenate(data, axis=0)  # Combine recorded chunks into one array
        sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)        

def merge_wav_files(system_file, microphone_file, output_file):
    try:
        data1, samplerate1 = sf.read(system_file)
        data2, samplerate2 = sf.read(microphone_file)

        if samplerate1 != samplerate2:
            raise ValueError("Sample rates do not match.")

        min_length = min(len(data1), len(data2))
        data1 = data1[:min_length]
        data2 = data2[:min_length]

        merged_data = (data1 + data2) / 2

        sf.write(output_file, merged_data, samplerate1)
        print("Merged file created:", output_file)
    except Exception as e:
        print("Error merging files:", e)

def start_recording():
    stop_recording.clear()

    system_thread = threading.Thread(target=record_system_audio)
    microphone_thread = threading.Thread(target=record_microphone_audio)

    system_thread.start()
    microphone_thread.start()

    return system_thread, microphone_thread


def stop_recording_threads(threads):
    stop_recording.set()
    for t in threads:
        t.join()
    print("Recording completed.")
    merge_wav_files("out_system.wav", "out_mikro.wav", "out_merged.wav")
    print("Merging completed.")

