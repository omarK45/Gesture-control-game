import math
import pickle
import os
from sklearn.svm import SVC
def calculate_angle(center, point):
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    return math.degrees(math.atan2(dy, dx))



def extract_features(defects, hand_contour, centroid):
    num_defects = len(defects)
    avg_depth = sum([d[3] for d in defects]) / num_defects if num_defects > 0 else 0
    angles = []
    for defect in defects:
        start_point, end_point, deepest_point, _ = defect
        start_angle = calculate_angle(centroid, start_point)
        end_angle = calculate_angle(centroid, end_point)
        angles.append(abs(start_angle - end_angle))
    avg_angle = sum(angles) / len(angles) if angles else 0
    return [num_defects, avg_depth, avg_angle]

class GestureClassifier:
    def __init__(self, model_path="gesture_model.pkl"):
        self.model_path = model_path
        self.model = None
        if os.path.exists(model_path):
            with open(model_path, 'rb') as file:
                self.model = pickle.load(file)
        else:
            self.model = SVC(kernel='linear')

    def train(self, feature_vectors, labels):
        self.model.fit(feature_vectors, labels)
        with open(self.model_path, 'wb') as file:
            pickle.dump(self.model, file)

    def predict(self, feature_vector):
        return self.model.predict([feature_vector])[0]

