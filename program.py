#!/usr/bin/env python

import sys
import json

from Prediction_Engine import Prediction_Engine
from CRF import CRF


def read_data_from_file(filepath):
    dataset = []
    f = open(filepath, 'r')
    for line in f:
        discussion = json.loads(line)
        dataset.append(discussion)
    return dataset


def read_data_from_terminal():
    dataset = []
    for line in sys.stdin:
        discussion = json.loads(line)
        dataset.append(discussion)
    return dataset


def write_data_to_file(dataset, filepath):
    f = open(filepath, 'w')
    for discussion in dataset:
        f.write(json.dumps(discussion) + '\n')


def write_data_to_termianl(dataset):
    for discussion in dataset:
        print(json.dumps(discussion))


if __name__ == '__main__':
    model = Prediction_Engine()
    crf = CRF()

    '''
    Training
    '''
    dataset1 = read_data_from_file('data/Dataset1.json')
    dataset2 = read_data_from_file('data/Dataset2.json')
    dataset3 = read_data_from_file('data/Dataset3.json')
    training_dataset = dataset1 + dataset2 + dataset3
    weakly_labeled_training_dataset = model.predict(training_dataset)

    predicted_dataset =\
        crf.train_and_predict(weakly_labeled_training_dataset,
                              weakly_labeled_training_dataset)

    '''
    Testing
    '''
    testing_dataset = read_data_from_terminal()
    weakly_labeled_testing_dataset = model.predict(testing_dataset)
    predicted_dataset = crf.predict(weakly_labeled_testing_dataset)
    # write_data_to_termianl(predicted_dataset)
    write_data_to_file(predicted_dataset, 'data/Predicted_Results.json')
