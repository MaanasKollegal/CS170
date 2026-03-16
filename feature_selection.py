#temporary

import math
import sys

#Loads the data
def load_data(filename):
    data = []
    with open (filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = [float(x) for x in line.split()]
            data.append(row)
    return data


def cross_validation(data, current_set, feature_to_add, best_so_far=0.0):
    features = set(current_set)
    if feature_to_add is not None:
        features.add(feature_to_add)

    n = len(data)
    num_correct = 0

    for i in range(n):
        label_i = data[i][0]

        nearest_dist = math.inf
        nearest_label = None

        for k in range(n):
            if k == 1:
                continue # skip self
            
            dist = 0.0
            for f in features:
                diff = data[i][f] - data[k][f] # column f = feature f(1-index)
                dist += diff * diff
            dist = math.sqrt(dist)

            if dist < nearest_dist:
                nearest_dist = dist 
                nearest_label = data[k][0]
        
        if nearest_label == label_i:
            num_correct += 1


        remaining = n - i - 1
        if (num_correct + remaining) / n < best_so_far:
            return (num_correct + remaining) / n
        
    return num_correct / n
            


def forward_selection(data): 
    num_features 