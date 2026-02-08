import pyttsx3
import speech_recognition as sr
import pyaudio
import wave
import datetime
import os
import pywhatkit as kit
from pytube import YouTube
from pydub import AudioSegment
import pygame
import cv2
import pyautogui
import time
import pyqrcode



def voice_change(audio):
    engine = pyttsx3.init()  # Initialize an instance
    voices = engine.getProperty('voices')  # Get the available voices
    engine.setProperty('voice', voices[1].id)  # Changing voice to index 1 for female voice
    engine.say(audio)  # Say method for passing text to be spoken
    print(audio)
    engine.runAndWait()  # Run and process the voice command


    

def record_audio(filename, duration=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("Audio saved to:", filename)

def recognize_speech(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    
    try:
        recognized_text = recognizer.recognize_google(audio_data, language="en-IN")
        recognized_text = recognized_text.lower()
        print("Recognized speech:", recognized_text)
        voice_change(recognized_text)  # Speak the recognized speech
        return recognized_text

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        voice_change("Sorry, I could not understand what you said.")
        return "no command"

    except sr.RequestError as e:
        print("Error fetching results from Google Speech Recognition service:", e)
        voice_change("I am having trouble connecting to the speech service.")
        return "no command"


def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        voice_change("Good Morning paaarth")
    elif 12 <= hour < 18:
        voice_change("Good afternoon paaarth")
    else:
        voice_change("Good Evening paaarth")
    voice_change("I am Jarvis please tell me how can I help you")


    

import speech_recognition as sr

def userecogniser(filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        # You can change language to "en-US" if you prefer
        recognized_text = recognizer.recognize_google(audio_data, language="en-IN")
        recognized_text = recognized_text.lower()
        print("Recognized speech:", recognized_text)

        # Speak back what user said (your existing behavior)
        voice_change(recognized_text)

        return recognized_text

    except sr.UnknownValueError:
        # When Google can't understand the audio
        print("[WARN] Could not understand audio. Please speak again.")
        voice_change("Sorry, I could not understand. Please say that again.")
        return ""   # return empty so caller can handle it

    except sr.RequestError as e:
        # When there is a network / API problem
        print(f"[ERROR] Could not request results from Google Speech Recognition service; {e}")
        voice_change("I am having trouble connecting to the speech service right now.")
        return ""


contacts = {
    "mummy": "+917859800818",
    "parth": "+919033910589",
    "didi": "+91..........",
    "papa": "+919727542123",
    "harpreet": "+91.........",
    "jenny mam" : "+91..........",
}


def recognize_speech(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
    try:
        recognized_text = recognizer.recognize_google(audio_data).lower()
        return recognized_text
    except sr.UnknownValueError:
        return "no command"







def command():
    filename = "recorded_audio.wav"
    filename1="recorded_audio1.wav"
    while True:
        record_audio(filename)
        recognized_text = userecogniser(filename)
        if not recognized_text:
                # Nothing understood, just ask again
                voice_change("Please speak the command again.")
                continue

        if "open powerpoint" in recognized_text:
                        path = "D:\\parth\\python\\didi.pptx"
                        os.startfile(path)
                        time.sleep(5)
                        pyautogui.hotkey('f5')
                        voice_change("Slideshow started automatically")
                        
                        waiting_for_next = True
                        
                        while True:
                            if waiting_for_next:
                                filename = "audio.wav"
                                record_audio(filename)
                                command = recognize_speech(filename)
                                
                                if "next" in command:
                                    pyautogui.press('enter')
                                    voice_change("next")
                                    waiting_for_next = False
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                elif "previous" in command:
                                    pyautogui.press('left')
                                    voice_change("previous")
                                    waiting_for_next = False
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                elif "exit" in command:
                                    os.system("taskkill /f /im POWERPNT.EXE")
                                    break  # Exit the loop and end the program
                                elif command == "no command":
                                    # Handle the case where no command is recognized
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                else:
                                    voice_change("Unrecognized command. Please try again.")
                                    continue  # Go back to the beginning of the loop to check for "next" again
                            else:
                                time.sleep(0.5)  # Wait for a short duration before checking again if "next" is spoken
                                filename = "audio.wav"
                                record_audio(filename)
                                command = recognize_speech(filename)  # Reuse the previous command
                                
                                if "next" in command:
                                    pyautogui.press('enter')
                                    voice_change("next")
                                    waiting_for_next = True
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                elif "previous" in command:
                                    pyautogui.press('left')
                                    voice_change("previous")
                                    waiting_for_next = True
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                elif "exit" in command:
                                    os.system("taskkill /f /im POWERPNT.EXE")
                                    break  # Exit the loop and end the program
                                elif command == "no command":
                                    # Handle the case where no command is recognized
                                    continue  # Go back to the beginning of the loop to check for "next" again
                                else:
                                    voice_change("Unrecognized command. Please try again.")
                                    continue  # Go back to the beginning of the loop to check for "next" again
                        exit()







                    
        elif "open whatsapp" in recognized_text:
            voice_change("Speak the name of the contact")
            record_audio(filename)
            recognized_text = userecogniser(filename)
            voice_change("Speak the message")
            record_audio(filename1)
            recognized_text1 = userecogniser(filename1)
            if recognized_text in contacts:
                now = datetime.datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                kit.sendwhatmsg(contacts[recognized_text], recognized_text1, current_hour, current_minute + 1)  # Adding 1 minute to current time
                print("Message sent successfully to", recognized_text)
                exit()
            else:
                 print("Contact not found.")
        elif "find a file" in recognized_text:
            voice_change("Speak a file name ")
            smain()
            exit()
        elif "play song" in recognized_text:
            parth()
            exit()

        voice_change("sorry sir i am unable to hear speak the command again")

        # elif "generate qr" in recognized_text:
        #         password = "012345678"
        #         security = "WPA"  # Adjust if using a different security protocol
        #         qr_filename = generate_wifi_qr(password, security)
        #         print(f"Wi-Fi QR code generated: {qr_filename}")


        




def generate_wifi_qr(password, security='WPA'):
    wifi_data = f"WIFI:T:{security};P:{password};;"
    qr = pyqrcode.create(wifi_data)
    qr.png('wifi_qr.png', scale=6)
    return 'wifi_qr.png'






def find_file_in_directory(directory, file_name):
    for root, _, files in os.walk(directory):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            print("File found at path:", file_path)
            return file_path
    print("File not found in the specified directory.")
    return None





def smain():
    directory = "D:\\"  # Assuming the directory is always D:\ for this case
    filename1="recorded_audio1.wav"
    record_audio(filename1)
    file_name = userecogniser(filename1)
    file_name = file_name + ".py"
    file_path = find_file_in_directory(directory, file_name)
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                voice_change(content) #forrrrr reading content of fileeeeeeeeee
                print("File content:\n", content)
        except Exception as e:
            print("Error:", e)







def parth():

    def download_audio(url, output_path):
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = output_path + audio_stream.default_filename
        if not os.path.exists(audio_file_path):
            audio_stream.download(output_path)
        return audio_file_path

    def convert_to_wav(audio_file_path):
        # Load the audio file
        audio = AudioSegment.from_file(audio_file_path)
        # Convert to wav format
        wav_audio = audio.export(audio_file_path[:-4] + ".wav", format="wav")
        return audio_file_path[:-4] + ".wav"

    def play_audio(audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()

    # Prompt the user to choose whether to download or play an existing song
    voice_change("Do you want to download a new song or play an existing one?")
    voice_change("speak  one to Download a new song")
    voice_change("speak  two to Play an existing song")
    filename1="recorded_audio1.wav"
    record_audio(filename1)
    file_name = userecogniser(filename1)
    choice = file_name

    # Fixed output directory
    output_path = 'D:/parth/python/'

    if "one" in choice or "1" in choice:
        # Prompt the user to enter the YouTube URL of the song
        youtube_url = input("Enter the YouTube URL of the song: ")
        # Download the audio from the YouTube video
        audio_file_path = download_audio(youtube_url, output_path)
    elif "tu" in choice or "2" in choice or "two" in choice or "to" in choice:
        voice_change("speak the name of the existing song (without extension): ")
        filename1="recorded_audio1.wav"
        record_audio(filename1)
        song_name = userecogniser(filename1)  # Prompt the user to enter the name of the existing song
        audio_file_path = output_path + song_name + ".mp4"
        # Check if the audio file exists
        if not os.path.exists(audio_file_path):
            voice_change("The specified song does not exist. Exiting...")
            exit()
    else:
        voice_change("Invalid choice. Exiting...")
        exit()

    # Convert to wav format if necessary
    if audio_file_path.endswith(".mp4"):
        audio_file_path = convert_to_wav(audio_file_path)

    # Play the audio
    play_audio(audio_file_path)

    # Listen for keyboard input to stop the song
    voice_change("Press Enter to stop the song.")
    input()  # Wait for Enter key press

    # Stop the playback
    pygame.mixer.music.stop()
    parth()



    import warnings
    warnings.filterwarnings("ignore")






def main():
    voice_change("speak paaarth or admin if you want  access ")
    filename1 = "recorded_audio.wav"
    record_audio(filename1)
    file_name = userecogniser(filename1)
    if "admin" in file_name or "parth" in file_name:

    
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trained_model.yml')  # Load your trained model here

        # Initialize webcam
        cap = cv2.VideoCapture(0)

        access_granted = False  

        while True:
            
            ret, frame = cap.read()

            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # For each detected face
            for (x, y, w, h) in faces:
                
                id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                
                if confidence < 70:  
                    # Draw a rectangle around the face
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                    if not access_granted:  # Only execute once if access is granted
                        voice_change("Access granted!")
                        
                        access_granted = True
                else:
                
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    # Deny access
                    print("Access denied!")
                    

            
            cv2.imshow('Face Recognition', frame)

            
            if access_granted:
                break

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        cap.release()
        cv2.destroyAllWindows()

        voice_change("welcome sir")
        filename = "recorded_audio.wav"
        record_audio(filename)
        recognize_speech(filename)
        wish()
        command()
    else:
        voice_change("you don't have access ")

        # Example usage
if __name__ == "__main__":
    main();
    