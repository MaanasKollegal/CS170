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
            data.append