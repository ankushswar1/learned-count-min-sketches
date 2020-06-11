import math
import numpy as np
import hashlib
import json 
import scipy.stats as stats
from CountMinSketch import CountMinSketch

class RuleCountMinSketch:
    def __init__(self, eps, delta, hh):
        self.eps = eps
        self.delta = delta
        self.cms = CountMinSketch(eps, delta)
        self.hh = hh
        self.perfect = {}

    def count(self, value):
        if value in self.hh:
            if str(value) in self.perfect:
                self.perfect[str(value)] = self.perfect[str(value)] + 1
            else:
                self.perfect[str(value)] = 1
        else:
            self.cms.count(value)

    def estimate(self, value):
        if (value in self.hh):
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