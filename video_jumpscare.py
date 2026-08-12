import cv2
import sys
import os
import numpy as np
from ffpyplayer.player import MediaPlayer

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



if __name__ == "__main__":
    video_jumpscare("explosion.mp4")