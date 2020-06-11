import math
import numpy as np
import hashlib
import json 
import scipy.stats as stats
from CountMinSketch import CountMinSketch
from sklearn.neural_network import MLPClassifier

class LearnedCountMinSketch:
    def __init__(self, eps, delta, train_data):
        self.eps = eps
        self.delta = delta
        self.cms = CountMinSketch(eps, delta)

        # set model
        X_train = train_data[0]
        Y_train = train_data[1]
        self.model = MLPClassifier(hidden_layer_sizes=(30, 40))
        self.model.fit(X_train.reshape(-1, 1), np.ravel(Y_train))
        self.perfect = {}

    def count(self, value):
        if (self.model.predict(np.array([value]).reshape(-1, 1)) == 1):
            if str(value) in self.perfect:
                self.perfect[str(value)] = self.perfect[str(value)] + 1
            else:
                self.perfect[str(value)] = 1
        else:
            self.cms.count(value)

    def estimate(self, value):
        if (self.model.predict(np.array([value]).reshape(-1, 1)) == 1):
            if str(value) in self.perfect: return self.perfect[str(value)]
            return 0
        else:
            return self.cms.estimate(value)

    def real_estimate(self, value):
        if str(value) in self.perfect: return self.perfect[str(value)]
        if str(value) in self.cms.backup: return self.cms.backup[str(value)]
        return -1

    def compute_size(self):
        size = 0
        for key in self.cms.backup:
            size += abs(self.cms.backup[key])
        for key in self.perfect:
            size += abs(self.perfect[key])
        return size

