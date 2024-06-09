import cv2
import numpy as np

class Camera:
    def __init__(self) -> None:
        self.camera = cv2.VideoCapture(2)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        _, self.frame = self.camera.read()
        self.frame = self.frame[70:-30, 140:-140, :]

    def get_frame(self):
        ret, self.frame = self.camera.read()
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        self.apply_pincushion_distortion(-0.6)
        self.apply_pincushion_distortion(0.3)
        # self.add_grid()

        self.frame = self.frame[70:-60, 140:-150, :]
        return self.frame

    def apply_pincushion_distortion(self, k1):
        h, w = self.frame.shape[:2]

        fx = w
        fy = h
        cx = w / 2
        cy = h / 2
        K = np.array([[fx, 0, cx],
                    [0, fy, cy],
                    [0, 0, 1]], dtype=np.float32)

        D = np.array([k1, 0, 0, 0], dtype=np.float32)
        map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, (w, h), cv2.CV_32FC1)
        self.frame = cv2.remap(self.frame, map1, map2, interpolation=cv2.INTER_LINEAR)


    def add_grid(self):
        row, col, c = self.frame.shape
        for x in range(0, row, 70):
            cv2.line(self.frame, (0, x), (col, x), (0, 255, 0), thickness=2)

        for y in range(0, col, 70):
            cv2.line(self.frame, (y, 0), (y, row), (0, 255, 0), thickness=2)
