import sklearn
import numpy as np
import MIDI_format
import sys
from sklearn.ensemble import RandomForestClassifier

def main():
    dir_name = sys.argv[1]

    return_list = MIDI_format.midi_to_datasets(dir_name,0.7,0.3)

    x_train = np.array(return_list[0])
    y_train = np.array(return_list[1])

    x_test = np.array(return_list[2])
    y_test = np.array(return_list[3])

    # x_train = x_train.reshape((x_train.shape[0], -1))
    # x_test = x_test.reshape((x_test.shape[0], -1))

    model = RandomForestClassifier(n_estimators=1000, max_depth=None, n_jobs=-1)
    model.fit(x_train, y_train)

    X_encode = model.encode(x_test)
    X_decode = model.decode(X_encode)

main()