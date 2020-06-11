import math
import numpy as np
import hashlib
import json 

class CountMinSketch:
    def __init__(self, eps, delta):
        self.eps = eps
        self.delta = delta
        self.w = math.ceil(np.exp(1) / eps)
        self.d = math.ceil(np.log(1 / delta))
        self.tables = np.zeros((self.d, self.w))
        self.backup = {}

    def compute_hash(self, value, table_no):
        fn = hashlib.md5()
        inp = str(value) + str(0) + str(table_no)
        fn.update(inp.encode())
        out = int(fn.hexdigest(), 16)
        return out % self.w

    def count(self, value):
        if str(value) in self.backup: 
            self.backup[str(value)] = self.backup[str(value)] + 1
        else:
            self.backup[str(value)] = 1
        for i in range(self.d):
            j = self.compute_hash(value, i)
            self.tables[i][j] = self.tables[i][j] + 1

    def estimate(self, value):
        ests = []
        for i in range(self.d):
            j = self.compute_hash(value, i)
            ests.append(self.tables[i][j])
        return min(ests)

    def real_estimate(self, value):
        if str(value) in self.backup: return self.backup[str(value)]
        return -1

    def compute_size(self):
        size = 0
        for key in self.backup:
            size += abs(self.backup[key])
        return size

    def save_counts(self, count_filename='counts.txt', actual_filename='backups.txt'):
        np.savetxt(count_filename, self.tables)
        with open(actual_filename, 'w') as fp: json.dump(self.backup, fp)

    def load_counts(self, count_filename='counts.txt', actual_filename='backups.txt'):
        with open(actual_filename, 'r') as fp: 
            temp = json.load(fp)
            self.backup = temp
        self.tables = np.loadtxt(count_filename)
