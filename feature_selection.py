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
 
#Evaluates accuracy of 1-NN using leave-one-out cross validation.
#Uses feature set = current_set + feature_to_add.
#best_so_far prunes a candidate if it cannot beat the current best accuracy
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

        #Find the nearest neighbor by comparing instance i to all others
        for k in range(n):
            if k == i:
                continue # skip self
            
            #Compute Euclidean distance using only the selected features
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

        #If the highest score from here can't beat best_so_far, stop
        remaining = n - i - 1
        if (num_correct + remaining) / n < best_so_far:
            return (num_correct + remaining) / n
        
    return num_correct / n
            

#Greedy forward search
#starts with an empty set and adds one feature
#at a time, always picking whichever feature improves accuracy the most.
def forward_selection(data): 
    num_features = len(data[0]) - 1

    #Evaluate accuracy using all features before search begins
    all_features = set(range(1, num_features + 1))
    full_acc = cross_validation(data, all_features, None)
    print(f"\nRunning nearest neighbor with all {num_features} features, "
          f"using \"leaving-one-out\" evaluation, I get an accuracy of {full_acc * 100:.1f}%")
    
    print("\nBeginning search.\n")

    current_set = set()
    best_overall_accuracy = 0.0
    best_overall_features = set()

    #Each level of the loop adds one feature to the current set
    for level in range(1, num_features + 1):
        best_accuracy_this_level = 0.0
        feature_to_add_this_level = None
 
        #Try adding each feature not already in the current set
        for f in range(1, num_features + 1):
            if f in current_set:
                continue
 
            accuracy = cross_validation(data, current_set, f, best_accuracy_this_level)
            candidate = current_set | {f}
            print(f"\t\tUsing feature(s) {set_str(candidate)} accuracy is {accuracy * 100:.1f}%")

            #Track the best feature to add at this level
            if accuracy > best_accuracy_this_level:
                best_accuracy_this_level = accuracy
                feature_to_add_this_level = f

        #Add the best feature found at this level
        current_set = current_set | {feature_to_add_this_level}

        #Warn if accuracy dropped, but keep searching in case of local maxima
        if best_accuracy_this_level < best_overall_accuracy:
            print(f"\n(Accuracy has decreased, continuing search in case of local maxima)")

        else: 
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = set(current_set)

            print(f"Feature set {set_str(current_set)} was best, accuracy is "
              f"{best_accuracy_this_level * 100:.1f}%\n")
            
    print(f"Finished search. Best feature subset is {set_str(best_overall_features)}, "
          f"which has an accuracy of {best_overall_accuracy * 100:.1f}%")
    

#Greedy backward search
#starts with all features and removes one feature at a time, always dropping whichever feature hurts accuracy the least.
def backwards_elimination(data):
    num_features = len(data[0]) - 1

    #start with full feature set
    current_set = set(range(1, num_features + 1))
    full_acc = cross_validation(data, current_set, None)
    print(f"\nRunning nearest neighbor with all {num_features} features, "
          f"using \"leaving-one-out\" evaluation, I get an accuracy of {full_acc * 100:.1f}%")
 
    print("\nBeginning search.\n")
 
    #Initialize best as the full feature set accuracy
    best_overall_accuracy = full_acc
    best_overall_features = set(current_set)
 
    #Each level of the loop removes one feature from the current set
    for level in range(1, num_features + 1):
        if len(current_set) == 0:
            break
 
        best_accuracy_this_level = 0.0
        feature_to_remove_this_level = None
 
        #Try removing each feature still in the current set
        for f in sorted(current_set):
            candidate = current_set - {f}
            if len(candidate) == 0:
                accuracy = 0.0
            else:
                accuracy = cross_validation(data, candidate, None, best_accuracy_this_level)
            print(f"\t\tUsing feature(s) {set_str(candidate)} accuracy is {accuracy * 100:.1f}%")
 
            #Track the best feature to remove at this level
            if accuracy > best_accuracy_this_level:
                best_accuracy_this_level = accuracy
                feature_to_remove_this_level = f

        #Remove the feature whose removal hurt accuracy the least
        current_set = current_set - {feature_to_remove_this_level}
 
        if best_accuracy_this_level < best_overall_accuracy:
            print(f"\n(Accuracy has decreased, continuing search.)")
        else:
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = set(current_set)
 
        print(f"Feature set {set_str(current_set)} was best, accuracy is "
              f"{best_accuracy_this_level * 100:.1f}%\n")
 
        if len(current_set) == 0:
            break
 
    print(f"Finished search, the best feature subset is {set_str(best_overall_features)}, "
          f"which has an accuracy of {best_overall_accuracy * 100:.1f}%")
 



def main():
    print("Welcome to Feature Selection Algorithm.")
 
    filename = input("Type in the name of the file to test: ").strip()
 
    try:
        data = load_data(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
 
    num_features = len(data[0]) - 1
    num_instances = len(data)
    print(f"\nThis dataset has {num_features} features (not including the class attribute), "
          f"with {num_instances} instances.\n")
 
    print("Type the number of the algorithm you want to run.")
    print("  1) Forward Selection")
    print("  2) Backward Elimination")
 
    choice = input("\n").strip()
 
    if choice == "1":
        forward_selection(data)
    elif choice == "2":
        backwards_elimination(data)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)
 
 
if __name__ == "__main__":
    main()