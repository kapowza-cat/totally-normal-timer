import time
import random
import tkinter as tk
import ctypes
import multiprocessing
from platform import system
import keyboard
import threading
from win11toast import toast
import cv2
import sys
import os
import numpy as np
from ffpyplayer.player import MediaPlayer

# Tell Windows to render at native DPI resolution
if system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
        except Exception:
            pass

#STRESS
# the following functions are ai generated because i am lazy
#
#
#

def lucas_lehmer(p, stop_flag):
    """
    Tests if M_p = 2^p - 1 is prime using the Lucas-Lehmer algorithm.
    Mimics the core mathematical verification function of Prime95.
    """
    if p == 2:
        return True
    
    # Mersenne number to test
    m_p = (1 << p) - 1
    
    # Initial state
    s = 4
    
    # Perform iterations (p - 2 times)
    for _ in range(p - 2):
        s = (s * s - 2) % m_p
        if stop_flag.is_set():
            break
        
    return s == 0

def stress_test_worker(worker_id, stop_flag):
    test_exponents = [9941, 11213, 19937, 21701, 23209, 44497]
    
    idx = 0
    while not stop_flag.is_set():
        p = test_exponents[idx % len(test_exponents)]
        
        start_time = time.time()
        is_prime = lucas_lehmer(p, stop_flag)
        duration = time.time() - start_time
        
        idx += 1

def stress_cpu(length):
    cpu_count = multiprocessing.cpu_count()
    
    manager = multiprocessing.Manager()
    stop_flag = manager.Event()
    processes = []
    
    # Spawn a worker process for every logical CPU core
    for i in range(cpu_count):
        p = multiprocessing.Process(target=stress_test_worker, args=(i, stop_flag))
        processes.append(p)
        p.start()
        
    try:
        # Run the stress test until manually stopped or time has passed
        start_time = time.perf_counter()
        while True:
            time.sleep(1)
            if time.perf_counter() - start_time >= length:
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        stop_flag.set()
        for p in reversed(processes):
            p.join()

#VIDEO_JUMPSCARE
# same as before
#
#
#
#

def video_jumpscare(path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    video_path = path
    video_path = os.path.join(base_path,video_path)
    window_name = "jumpscare"

    cap = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while cap.isOpened():
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()

        if not ret or val == 'eof':
            break  
            
        if val == 'paused':
            continue

        cv2.imshow(window_name, frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    try:
        black_screen = np.zeros((1080, 1920, 3), dtype=np.uint8)
        cv2.imshow(window_name, black_screen)
        cv2.waitKey(1)
    except:
        pass


    try:
        player.set_pause(True)
        player.close_player()
    except:
        pass

    cap.release()
    cv2.destroyWindow("jumpscare")

#now this is my code

class FloatingTimer:

    def __init__(self, root):
        self.root = root

        # alwaysontop
        self.root.wm_attributes("-topmost", True)
        self.root.overrideredirect(True)

        # window dimensions
        window_width = 180
        window_height = 60

        # dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Variable init
        # visibility
        #
        #
        #
        #
        #
        #
        self.isTimerPaused = False
        self.start_of_pause = 0
        self.timer_mode = 's'
        self.should_stop = False
        self.wackymode = False
        self.lengthOfSecond = 1
        self.isStressTestRunning = False

        # x/y
        padding_right = 0
        taskbar_offset = 60  # change this if needed

        x_coordinate = screen_width - window_width - padding_right
        y_coordinate = screen_height - window_height - taskbar_offset

        #WidthxHeight+X+Y
        self.root.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}"
        )
        self.root.configure(bg="#333333")

        #display label
        self.label = tk.Label(
            root,
            text="",
            font=("Calibri", 28, "bold"),
            fg="#00FF66",
            bg="#333333",
        )
        self.label.pack(expand=True)

        # bindings
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        self.root.bind("<Button-2>", lambda e: self.root.destroy())
        self.root.bind("<Button-3>", self.pause_timer)

        self.start_time = time.time()
        thread1 = threading.Thread(target=self.input, daemon=True)
        thread1.start()

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def input(self):
        self.label.config(text="T/S")
        input = ''
        # listen for t/s
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'esc':
                    self.root.destroy()
                if event.name == 't' or event.name == 's' or event.name == 'S':
                    input = event.name
                    break
        self.timer_mode = input
        if input == 's':
            self.wackymode = False
            self.start_time = time.time()
            self.time_tracker()
        elif input == 'S':
            self.wackymode = True
            self.start_time = time.time()
            self.time_tracker()
        else:
            thread2 = threading.Thread(target=self.input2, daemon=True)
            thread2.start()

    def input2(self):
        self.root.after(0, lambda: self.label.config(text="--:--:--"))
        digits = []

        while True:
            event = keyboard.read_event()

            if event.event_type != keyboard.KEY_DOWN:
                continue

            key_name = event.name

            if key_name == "esc":
                self.root.after(0, self.root.destroy)
                return

            if key_name == "enter":
                if digits:
                    if keyboard.is_pressed('shift'):
                        self.wackymode = True
                    break
                continue

            if key_name == "backspace":
                if digits:
                    digits.pop()

            else:
                last_char = key_name[-1]
                if last_char.isdigit() and len(digits) < 6:
                    digits.append(last_char)
            padded = ["-"] * (6 - len(digits)) + digits
            formatted_str = f"{padded[0]}{padded[1]}:{padded[2]}{padded[3]}:{padded[4]}{padded[5]}"

            self.root.after(0, lambda text=formatted_str: self.label.config(text=text))

        time_str = "".join(digits).zfill(6)  # 6 digits
        hours = int(time_str[0:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])

        self.total_seconds = (hours * 3600) + (minutes * 60) + seconds
        self.start_time = time.time()

        self.time_tracker()

    def pause_timer(self, *args):
        self.startofpause = time.perf_counter()
        if not self.isTimerPaused:
            self.isTimerPaused = True
            self.start_of_pause = time.time()
        else:
            self.isTimerPaused = False
            end_of_pause = time.time()
            paused_for = end_of_pause - self.start_of_pause
            self.start_time += paused_for

    def end(self):
        self.should_stop = True
        self.label.config(text="00:00")
        time.sleep(1)
        while True:
            self.label.config(text="")
            time.sleep(0.5)
            self.label.config(text="00:00")
            time.sleep(0.5)

    def update_timer(self):
        if self.should_stop:
            return
        elapsed = int(self.mainTimeCount)
        if self.timer_mode == 't':       
            elapsed = self.total_seconds - elapsed
            if elapsed == 0:
                thread3 = threading.Thread(target=self.end, daemon=True)
                thread3.start()
                return
        seconds = elapsed % 60
        minutes = (elapsed // 60) % 60
        hours = elapsed // 3600
        if self.isTimerPaused:
            return
        if elapsed >= 3600:
            self.label.config(text=f"{hours:d}:{minutes:02d}:{seconds:02d}")
        else:
            self.label.config(text=f"{minutes:02d}:{seconds:02d}")

    def send_update_simple(self):
        self.updateThread = threading.Thread(target=self.update_timer, daemon=True)
        self.updateThread.start()

    def wacky(self, clock):
        if (random.randint(1,100) <= 90):
            self.send_update_simple()
            return

        choice = random.randint(1,100)
        

        if choice <= 10: #up
            self.lengthOfSecond = self.lengthOfSecond / 1.5
        elif choice <= 20: #down
            self.lengthOfSecond = self.lengthOfSecond * 1.5
        elif choice <= 30: #freeze
            time.sleep(self.lengthOfSecond * 5)
            self.mainTimeCount += 3
        elif choice <= 35: # swap
            self.mainTimeCount -= 1
            if self.timer_mode == 't':
                clock = self.total_seconds - self.mainTimeCount
            else:
                clock = self.mainTimeCount

            minutes = (clock // 60) % 60
            seconds = clock % 60

            swapped_clock = (seconds * 60) + minutes
            diff = swapped_clock - clock
            
            if self.timer_mode == 't':
                self.mainTimeCount -= diff
            else:
                self.mainTimeCount += diff
        elif choice <= 40: #jumpscare
            video_jumpscare("explosion.mp4")
        elif choice <= 45: #cpu go boom
            stress_cpu(15)
        elif choice <= 50: #draw cards until
            while not random.randint(1,70) == 1:
                self.mainTimeCount += 1
                self.send_update_simple()
                time.sleep(0.02)
        elif choice <= 55: #lay cards until
            while not random.randint(1,70) == 1:
                self.mainTimeCount -= 1
                self.send_update_simple()
                time.sleep(0.02)
        elif choice <= 77: #skip
            self.mainTimeCount -= random.randint(3,10)
        elif choice <= 99: #also skip
            self.mainTimeCount += random.randint(3,10)
        else:
            toast("The game", "More specifically, the one you just lost")
        
        if self.lengthOfSecond < 0.01:
            self.lengthOfSecond = 0.01
        if self.lengthOfSecond > 2.5:
            self.lengthOfSecond = 2.5
        

        self.send_update_simple()

    def time_tracker(self):
        self.mainTimeCount = 0
        self.send_update_simple()

        while True:
            self.startofsecond = time.perf_counter()

            time.sleep(self.lengthOfSecond) 
            # hurts to use time.sleep 
            # but it's the most accurate and simple method i've found so far

            if self.isTimerPaused:
                while self.isTimerPaused:
                    time.sleep(0.05)

            if self.should_stop == True:
                break
            self.mainTimeCount += 1

            if self.wackymode:
                self.wacky(self.mainTimeCount)
            else:
                self.send_update_simple()



if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingTimer(root)
    root.mainloop()