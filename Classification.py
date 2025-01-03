



import cv2
import numpy as np


from hand_countours import *
from convex_hull import *
from Dataset_Creation import *
from CoG import *

from convexity_defects import *

import pickle
                                                    
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def classify():
    features = []
    c=0
    input_folder = ["datasets/open_palm" , "datasets/peace_2" , "datasets/khalid_gun" ,"datasets/segmented_3", "datasets/peace_kaddah" , "datasets/gun_ziad", "datasets/khalid_three", "datasets/gun_kaddah" ]
    for i in range(len(input_folder)):
            
        for filename in os.listdir(input_folder[i]):
            
            input_path = os.path.join(input_folder[i], filename)
            
            image = cv2.imread(input_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Shape: (256, 256)
            _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
            # cv2.imshow("image",image)
            # print(image.shape)
            c+=1
            print(c)
            contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Sort contours by area
            sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

            # Use the function to find the hand contour
            hand_contour,aspect_ratio = find_hand_contour(sorted_contours, image)
            hull = convex_hull(hand_contour)
            convex_hull_area = cv2.contourArea(np.array(hull, dtype=np.int32))
            contour_area = cv2.contourArea(hand_contour)
            contour_hull_ratio = contour_area / convex_hull_area
            points = [(p[0][0], p[0][1]) if isinstance(p[0], np.ndarray) else tuple(p[0]) for p in hand_contour]
            centeroid = calculate_centroid(points)
            defects = compute_convexity_defects(hand_contour,hull)
            num_defects = len(defects)
            perimeter = cv2.arcLength(hand_contour, True)
            circularity = (4 * np.pi * contour_area) / (perimeter ** 2)
            #["datasets/open_palm" 
            # , "datasets/peace_2" , 
            # "datasets/khalid_gun" ,
            # "datasets/segmented_3",
            # "datasets/peace_kaddah" ,
            # "datasets/gun_ziad", 
            # "datasets/khalid_three", 
            # "datasets/gun_kaddah" ]
            if i==0:
                label = "open palm"
            elif i == 1:
                label="peace"
            elif i == 2:
                label = "gun"       
            elif i == 3:
                label ="three"
                
            elif i== 4:
                label = "peace"
                
            elif i == 5:
                label = "gun"
            elif i == 6:
                label = "three"
                
            elif i == 7:
                label = "gun"
                
                
                
                
                
             
             
            features.append([num_defects, contour_hull_ratio, aspect_ratio,circularity,label])
            
    # Convert to DataFrame
    columns = ["Num_Convexity_Defects", "Contour_Hull_Ratio", "Aspect_Ratio", "Circularity", "Type"]
    df = pd.DataFrame(features, columns=columns)

    # Save to CSV
    df.to_csv("datasets/five_tained.csv", index=False)

        
        

        
    ###########################################################################################################################
                                                        ##svm##       
                                                        
                                                        
 

    # Load dataset
    df = pd.read_csv("datasets/five_tained.csv")
    X = df.drop(columns=["Type"])
    y = df["Type"]  # Labels (e.g., "Open Palm", "Fist")
    print(len(X))
    print(len(y))

    # # Split and scale data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train the SVM
    svm = SVC(kernel='rbf', C=1.0, gamma='scale')
    svm.fit(X_train, y_train)


    # Save SVM and scaler after training in classification file
    with open("datasets/svm_model.pkl", "wb") as model_file:
        pickle.dump(svm, model_file)
    with open("datasets/scaler.pkl", "wb") as scaler_file:
        pickle.dump(scaler, scaler_file)


    # Evaluate the SVM
    print("Accuracy:", svm.score(X_test, y_test))
#classify()