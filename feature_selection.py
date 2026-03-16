
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


#Format a set of feature numbers as {a,b,c} sorted.
def set_str(s):
    return "{" + ",".join(str(x) for x in sorted(s)) + "}"
 

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
            if k == i:
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
    num_features = len(data[0]) - 1

    all_features = set(range(1, num_features + 1))
    full_acc = cross_validation(data, all_features, None)
    print(f"\nRunning nearest neighbor with all {num_features} features, "
          f"using \"leaving-one-out\" evaluation, I get an accuracy of {full_acc * 100:.1f}%")
    
    print("\nBeginning search.\n")

    current_set = set()
    best_overall_accuracy = 0.0
    best_overall_features = set()

    for level in range(1, num_features + 1):
        best_accuracy_this_level = 0.0
        feature_to_add_this_level = None
 
        for f in range(1, num_features + 1):
            if f in current_set:
                continue
 
            accuracy = cross_validation(data, current_set, f, best_accuracy_this_level)
            candidate = current_set | {f}
            print(f"\t\tUsing feature(s) {set_str(candidate)} accuracy is {accuracy * 100:.1f}%")

            if accuracy > best_accuracy_this_level:
                best_accuracy_this_level = accuracy
                feature_to_add_this_level = r

        current_set = current_set | {feature_to_add_this_level}

        if best_accuracy_this_level < best_overall_accuracy:
            print(f"\n(Accuracy has decreased, continuing search in case of local maxima)")

        else: 
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = set(current_set)

            print(f"Feature set {set_str(current_set)} was best, accuracy is "
              f"{best_accuracy_this_level * 100:.1f}%\n")
            
    print(f"Finished search. Best feature subset is {set_str(best_overall_features)}, "
          f"which has an accuracy of {best_overall_accuracy * 100:.1f}%")