import eel
import speech_recognition as sr
import pyaudio
import wave

@eel.expose
def recog():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 7
    filename = "/Users/marcus/Desktop/Skap/useless-voice-assistant/record.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording-In-Progress...')

    stream = p.open(format=sample_format,channels=channels,rate=fs,frames_per_buffer=chunk,input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for _ in range(int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Recording-Finnished.')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    text = ""

    r = sr.Recognizer()
    filename = "/Users/marcus/Desktop/Skap/useless-voice-assistant/record.wav"
    # open the file
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        try:
            text = r.recognize_google(audio_data)
            print(f"Text-Recognized: '{text}'")
        except Exception:
            text = "try again"
            print("No-Audio-Recognized")
    return text 

eel.init('web')
eel.start('intro.html', cmdline_args=['--start-fullscreen'])
