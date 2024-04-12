import pickle

import numpy as np

from image_processing import process_image


labels_dict = {0: 'A', 1: 'B', 3: 'D', 6: 'G'}


def translate(image_path, model_path):

    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']

    hand_landmarks = process_image(image_path)

    prediction = model.predict(np.asarray(hand_landmarks))

    predicted_character = labels_dict[int(prediction[0])]

    return predicted_character
