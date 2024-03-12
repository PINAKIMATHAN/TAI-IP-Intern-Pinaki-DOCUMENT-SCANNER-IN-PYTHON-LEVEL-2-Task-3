import cv2
import numpy as np
import pyautogui
import tkinter as tk
import threading
from tkinter import filedialog

class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.resolution = (1920, 1080)
        self.fps = 15
        self.codec = cv2.VideoWriter_fourcc(*"XVID")
        self.video_output = None
    def start_recording(self):
        self.recording = True
        while self.recording:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mouse_x, mouse_y = pyautogui.position()

            cv2.circle(frame, (mouse_x, mouse_y), 5, (0, 0, 255), -1)

            self.video_output.write(frame)
        self.video_output.release()
    def stop_recording(self):
        self.recording = False

recorder = ScreenRecorder()

def start_recording():
    start_button["state"] = tk.DISABLED
    stop_button["state"] = tk.NORMAL
    
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
    if not file_path:
        start_button["state"] = tk.NORMAL
        stop_button["state"] = tk.DISABLED
        return
    
    recorder.video_output = cv2.VideoWriter(file_path, recorder.codec, recorder.fps, recorder.resolution)
    
    window.iconify()
    
    recording_thread = threading.Thread(target=recorder.start_recording)
    recording_thread.start()

def stop_recording():
    start_button["state"] = tk.NORMAL
    stop_button["state"] = tk.DISABLED
    recorder.stop_recording()

window = tk.Tk()
window.title("ScRecor")
window.iconbitmap("iconFilm.ico")
window.configure(bg="#189100")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window.winfo_reqwidth() / 2))
y_coordinate = int((screen_height / 2) - (window.winfo_reqheight() / 2))

window.geometry(f"+{x_coordinate}+{y_coordinate}")

window.resizable(False, False)

start_button = tk.Button(window, text="Start Recording", command=start_recording)
start_button.pack(side=tk.LEFT, padx=10, pady=10)

stop_button = tk.Button(window, text="Stop Recording", command=stop_recording, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT, padx=10, pady=10)

window.mainloop()
