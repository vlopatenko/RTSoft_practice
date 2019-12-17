import numpy as np
import cv2


def draw_circle(x, frame):
    cv2.circle(frame, center=(int(x[1]), int(x[0])), radius=5, color=[0, 0, 255], thickness=-1)


def main():
    cap_in = cv2.VideoCapture('video.mp4')

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    size = int(cap_in.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap_in.get(cv2.CAP_PROP_FPS))

    cap_out = cv2.VideoWriter('output.mp4', fourcc=fourcc, fps=fps, frameSize=size)

    if not cap_in.isOpened():
        raise IOError('Cannot open input video')

    if not cap_out.isOpened():
        raise IOError('Cannot open output video')

    ESC = 27

    while True:
        ret, frame = cap_in.read()

        if not ret:
            break

        # Переводим кадр в grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Применяем размытие для сглажвивания несущественных переходов,
        # которые могут быть приняты за контур
        blurred = cv2.GaussianBlur(gray, ksize=(5, 5), sigmaX=10, sigmaY=10)

        # Переводим из grayscale в черно-белое
        ret, thresh = cv2.threshold(blurred, thresh=96, maxval=255, type=cv2.THRESH_BINARY)

        # Находим контуры
        contours, hierarchy = cv2.findContours(thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            cv2.drawContours(frame, contours, contourIdx=-1, color=(0, 255, 0), thickness=3)

            # Находим контур с максимальной площадью
            nb_contour = max(contours, key=cv2.contourArea)

            rect = cv2.minAreaRect(nb_contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

        cap_out.write(frame)

        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == ESC:
            break

    cap_in.release()
    cap_out.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
