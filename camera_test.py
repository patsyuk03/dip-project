import cv2
import numpy as np

def apply_pincushion_distortion(image, k1):
    """
    Applies pincushion distortion to an image.

    Parameters:
    image (numpy.ndarray): Input image.
    k1 (float): Distortion coefficient. Positive values for pincushion distortion.

    Returns:
    numpy.ndarray: Distorted image.
    """
    # Get the dimensions of the image
    h, w = image.shape[:2]

    # Generate the camera matrix
    fx = w
    fy = h
    cx = w / 2
    cy = h / 2
    K = np.array([[fx, 0, cx],
                  [0, fy, cy],
                  [0, 0, 1]], dtype=np.float32)

    # Generate the distortion coefficients array
    D = np.array([k1, 0, 0, 0], dtype=np.float32)

    # Generate the map for remapping the pixels
    map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, (w, h), cv2.CV_32FC1)

    # Apply the remap to the image
    distorted_image = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR)

    return distorted_image    

def add_grid(frame):
    row, col, c = frame.shape
    for x in range(0, row, 70):
        cv2.line(frame, (0, x), (col, x), (0, 255, 0), thickness=2)

    for y in range(0, col, 70):
        cv2.line(frame, (y, 0), (y, row), (0, 255, 0), thickness=2)

    return frame



def main():
    camera = cv2.VideoCapture(2)

    while True:
        ret, frame = camera.read()

        # frame = add_grid(frame)

        # frame = apply_pincushion_distortion(frame, 0.4)
        frame = apply_pincushion_distortion(frame, -0.6)
        frame = apply_pincushion_distortion(frame, 0.3)

        frame = add_grid(frame)

        cv2.imshow("Window 1", frame)

        # Quit the program when "q" is pressed
        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            break

    camera.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()