import keras
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import tensorflow as tf


def train_model(data_pickle_path):
    data_dictionary = pickle.load(open(data_pickle_path, 'rb'))

    data = np.asarray(data_dictionary['data'])
    labels = np.asarray(data_dictionary['labels'])

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

    model = RandomForestClassifier()

    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    score = accuracy_score(y_test, y_pred)

    print('{}% of correctly classified data'.format(score * 100))

    f = open('fingerspelling_classifier.pickle', 'wb')
    pickle.dump({'model': model}, f)
    f.close()