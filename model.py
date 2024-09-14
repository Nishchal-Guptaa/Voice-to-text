import pyttsx3
import speech_recognition as sr
import datetime
from googletrans import Translator
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

r = sr.Recognizer()
root = tk.Tk()
root.title("Speech Recognition For Indian Language")

output_text_widget = tk.Text(root, height=10, width=40)
output_text_widget.pack()

recording = False
paused = False
test_output = ''
selected_language = 'hi'

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def start_recording():
    global recording, test_output
    recording = True
    test_output = ''
    output_text_widget.delete(1.0, tk.END)

def stop_recording():
    global recording
    recording = False
    messagebox.showinfo("Info", "Recording Stopped")

def download_text():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"output_{current_time}.txt"
    with open(file_name, 'w') as t_f2:
        t_f2.write(test_output)
    messagebox.showinfo("Info", f"All recognized text saved to {file_name}")

def pause_recording():
    global paused
    paused = True
    messagebox.showinfo("Info", "Recording Paused")

def resume_recording():
    global paused
    paused = False
    messagebox.showinfo("Info", "Recording Resumed")

def change_language():
    global selected_language
    selected_language = language_var.get()
    messagebox.showinfo("Info", f"Translation language changed to {selected_language}")

start_button = ttk.Button(root, text="Start", command=start_recording)
stop_button = ttk.Button(root, text="Stop", command=stop_recording)
download_button = ttk.Button(root, text="Download", command=download_text)
pause_button = ttk.Button(root, text="Pause", command=pause_recording)
resume_button = ttk.Button(root, text="Resume", command=resume_recording)
language_label = ttk.Label(root, text="Translation Language:")
language_var = tk.StringVar(root)
language_combobox = ttk.Combobox(root, textvariable=language_var, values=('hi', 'en'))
change_language_button = ttk.Button(root, text="Change Language", command=change_language)

start_button.pack()
stop_button.pack()
download_button.pack()
pause_button.pack()
resume_button.pack()

language_label.pack()
language_combobox.pack()
change_language_button.pack()

language_var.set(selected_language)

def listen():
    global recording, test_output, paused, selected_language
    translator = Translator()
    while True:
        if recording and not paused:
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source)
                    mytext = r.recognize_google(audio).lower()

                    translation = translator.translate(mytext, dest=selected_language)
                    translated_text = translation.text

                    output_text_widget.insert(tk.END, f"Did you say: {mytext} ({selected_language} : {translated_text})\n")
                    output_text_widget.update()

                    test_output += mytext + '\n'

                    speak_text(mytext)
                    speak_text(translated_text)

                    if mytext == '001':
                        stop_recording()
                        download_text()
                        break

            except sr.RequestError as e:
                output_text_widget.insert(tk.END, f"Could not request result; {e}\n")
                output_text_widget.update()
            except sr.UnknownValueError:
                output_text_widget.insert(tk.END, "Unknown error occurred\n")
                output_text_widget.update()

def speech_thread():
    while True:
        listen()

speech_recognition_thread = threading.Thread(target=speech_thread)
speech_recognition_thread.daemon = True
speech_recognition_thread.start()

root.mainloop()
