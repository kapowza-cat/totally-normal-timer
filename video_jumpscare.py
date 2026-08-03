import cv2
import numpy as np
import os
from ffpyplayer.player import MediaPlayer

def video_jumpscare(path):
    video_path = path
    window_name = "You just lost the game"

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
    cv2.destroyWindow("You just lost the game")



if __name__ == "__main__":
    video_jumpscare("explosion.mp4")