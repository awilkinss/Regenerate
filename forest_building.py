import sklearn
import numpy as np
import MIDI_format
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn import preprocessing
from IPython.display import Image
import graphviz
from subprocess import call


def main():
    dir_name = sys.argv[1]
    train_list = []
    test_list = []
    labels = []

    return_list = MIDI_format.midi_to_datasets(dir_name,0.7,0.3)
    train_list,test_list,labels = convert(return_list)

    forest,encoder,decoder = create_model(train_list,test_list)

    display(forest,labels)

def convert(return_list):
    labels = []
    le = preprocessing.LabelEncoder()
    
    x_train = np.array(return_list[0])
    y_train = np.array(return_list[1])
    for i in range(x_train.shape[1]):
        print("current column:",x_train[:,i])
        x_train[:,i] = le.fit_transform(x_train[:,i])
    labels = y_train
    y_train = le.fit_transform(y_train)


    x_test = np.array(return_list[2])
    y_test = np.array(return_list[3])
    for i in range(x_test.shape[1]):
        print("current column:",x_test[:,i])
        x_test[:,i] = le.fit_transform(x_test[:,i])
    y_test = le.fit_transform(y_test)


    x_train = x_train.reshape((x_train.shape[0],-1))
    x_test = x_test.reshape((x_test.shape[0],-1))

    return [x_train,y_train],[x_test,y_test],labels

def create_model(train_list,test_list):

    x_train = train_list[0]
    y_train = train_list[1]
    x_test = test_list[0]
    y_test = test_list[1]

    model = RandomForestClassifier(n_estimators=10, max_depth=None, n_jobs=-1)
    model.fit(x_train, y_train)

    X_encode = model.encode(x_test)
    X_decode = model.decode(X_encode)

    return model,X_encode,X_decode

def display(fitted_forest,labels):
    estimator = fitted_forest.estimators_[5]

    # Export as dot file
    export_graphviz(estimator, out_file='tree.dot', 
                    feature_names = ['pitches','note duration','velocity'],
                    class_names = labels,
                    rounded = True, proportion = False, 
                    precision = 2, filled = True)

    # Convert to png using system command (requires Graphviz)
    call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

    # Display in jupyter notebook
    Image(filename = 'tree.png')

main()