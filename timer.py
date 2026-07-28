import time
import tkinter as tk
import ctypes
import platform
import keyboard
import threading

# Tell Windows to render at native DPI resolution (crisp text)
if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor DPI aware
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
        except Exception:
            pass


class FloatingTimer:

    def __init__(self, root):
        self.root = root

        # Keep window always on top & remove title bar
        self.root.wm_attributes("-topmost", True)
        self.root.overrideredirect(True)

        # Define window dimensions
        window_width = 180
        window_height = 60

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Variable init
        self.isTimerPaused = False
        self.start_of_pause = 0
        self.timer_mode = 's'

        # Calculate X and Y coordinates
        padding_right = 0
        taskbar_offset = 60  # Adjust if your taskbar is taller/shorter

        x_coordinate = screen_width - window_width - padding_right
        y_coordinate = screen_height - window_height - taskbar_offset

        # Set geometry: "WidthxHeight+X+Y"
        self.root.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}"
        )
        self.root.configure(bg="#333333")

        # Configure display label
        self.label = tk.Label(
            root,
            text="",
            font=("Calibri", 28, "bold"),
            fg="#00FF66",
            bg="#333333",
        )
        self.label.pack(expand=True)

        # Dragging & Exit bindings
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
                if event.name == 't' or event.name == 's':
                    input = event.name
                    break
        self.timer_mode = input
        if input == 's':
            self.start_time = time.time()
            self.update_timer()
        else:
            thread2 = threading.Thread(target=self.input2, daemon=True)
            thread2.start()

    def input2(self):
        # Safely set initial display text on the main thread
        self.root.after(0, lambda: self.label.config(text="--:--:--"))

        # Stores up to 6 digits (HHMMSS)
        digits = []

        while True:
            event = keyboard.read_event()

            # Only process KEY_DOWN events
            if event.event_type != keyboard.KEY_DOWN:
                continue

            key_name = event.name

            # 1. Exit on ESC
            if key_name == "esc":
                self.root.after(0, self.root.destroy)
                return

            # 2. Confirm and start timer on ENTER
            if key_name == "enter":
                if digits:  # Only proceed if at least one digit was entered
                    break
                continue

            # 3. Handle BACKSPACE (remove last entered digit)
            if key_name == "backspace":
                if digits:
                    digits.pop()

            # 4. Handle DIGITS (Standard numbers & Numpad)
            else:
                # Check if the last character of key_name is a digit (handles '1' and 'keypad 1')
                last_char = key_name[-1]
                if last_char.isdigit() and len(digits) < 6:
                    digits.append(last_char)

            # Build the padded HH:MM:SS format (e.g., typing '1', '2', '3' -> '--:01:23')
            padded = ["-"] * (6 - len(digits)) + digits
            formatted_str = f"{padded[0]}{padded[1]}:{padded[2]}{padded[3]}:{padded[4]}{padded[5]}"

            # Update the Tkinter label safely on the main thread
            self.root.after(0, lambda text=formatted_str: self.label.config(text=text))

        # Calculate total timer duration in seconds once ENTER is pressed
        time_str = "".join(digits).zfill(6)  # Ensures 6 characters (e.g., '000123')
        hours = int(time_str[0:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])

        self.total_seconds = (hours * 3600) + (minutes * 60) + seconds
        self.start_time = time.time()

        # Start the countdown on the main loop
        self.root.after(0, self.update_timer)

    def pause_timer(self, *args):
        if not self.isTimerPaused:
            self.isTimerPaused = True
            self.start_of_pause = time.time()
        else:
            self.isTimerPaused = False
            end_of_pause = time.time()
            paused_for = end_of_pause - self.start_of_pause
            self.start_time += paused_for

    def end(self):
        self.label.config(text="00:00")
        time.sleep(1)
        while True:
            self.label.config(text="")
            time.sleep(0.5)
            self.label.config(text="00:00")
            time.sleep(0.5)

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        if self.timer_mode == 't':       
            elapsed = self.total_seconds - elapsed
            if elapsed == 0:
                thread3 = threading.Thread(target=self.end, daemon=True)
                thread3.start()
                return
        seconds = elapsed % 60
        minutes = (elapsed // 60) % 60
        hours = elapsed // 3600
        if not self.isTimerPaused:
            if elapsed >= 3600:
                self.label.config(text=f"{hours:d}:{minutes:02d}:{seconds:02d}")
            else:
                self.label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.root.after(1000, self.update_timer)
        else:
            self.root.after(1000, self.update_timer)



if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingTimer(root)
    root.mainloop()