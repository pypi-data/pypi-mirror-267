import cv2
import mediapipe as mp
import numpy as np

from dataset_creator import hand


def process_image(image_path: str):

    image = cv2.imread(image_path)

    temp = []
    norm_x = []
    norm_y = []

    H, W, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    results = hand.process(image_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                norm_x.append(x)
                norm_y.append(y)

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x = x - min(norm_x)
                y = y - min(norm_y)

                temp.append(x)
                temp.append(y)

        x1 = int(min(norm_x) * W) - 10
        y1 = int(min(norm_y) * H) - 10

        x2 = int(max(norm_x) * W) - 10
        y2 = int(max(norm_y) * H) - 10

    return temp
