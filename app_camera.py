import os
os.environ["OPENCV_VIDEOIO_MSFS_ENABLE_HW_TRANSFORMS"] = "0"

import cv2
from cv2 import aruco
import numpy as np

BLACK = (0,0,0)
RED = (0,0,255)
GREEN = (0,255,0)
BLUE = (255,0,0)
WHITE = (255,255,255)

class Camera():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.dic_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.last_frame = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)

    def find_cards(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame
        else:
            frame = self.last_frame

        # 区画線
        cv2.line(frame, (0, self.HEIGHT//2), (self.WIDTH, self.HEIGHT//2), RED, 1)
        cv2.line(frame, (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT), RED, 1)

        # マーカー検出
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = aruco.detectMarkers(gray, self.dic_aruco)
        list_ids = np.ravel(ids)
        if len(list_ids) > 1:
            print(len(list_ids))

        for id, corner in zip(list_ids, corners):
            pts = np.int32(corner[0])
            frame = cv2.polylines(frame, [pts], True, GREEN, 2)
            frame = self.find_word_area(frame, pts)
        
        self.frame = frame

    def find_word_area(self, frame, pts):
        # マーカーの座標とベクトル
        mp0, mp1, mp2, mp3 = map(np.array, pts)         # 各頂点をnumpy配列で定義する
        vw, vh = mp1 - mp0, mp3 - mp0                   # マーカーの横と縦のベクトル

        # マーカーが画面（ベース）上のどこにあるか
        cp = np.array((self.WIDTH//2, self.HEIGHT//2))  # フレームの中心
        diff = mp2 - cp                                 # フレーム中心からマーカーまでのベクトル
        signs = (diff[0] > 0, diff[1] > 0)              # ベクトルのxとyの正負
        if signs == (False, False):
            position = "左上"
        elif signs == (True, False):
            position = "右上"
        elif signs == (False, True):
            position = "左下"
        else:
            position = "右下"
        print(position)
        # 単語エリアを定義
        tp0 = mp2
        tp1 = tp0 + 5 * vw
        tp3 = tp0 + 8 * vh
        tp2 = tp0 + 5 * vw + 8 * vh
        text_pts = np.int32([tp0, tp1, tp2, tp3])
        cv2.polylines(frame, [text_pts], True, BLUE, 2)
        return frame

    def show(self):
        cv2.imshow("camera", self.frame)

def main():
    camera = Camera()
    while True:
        camera.find_cards()
        camera.show()
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()