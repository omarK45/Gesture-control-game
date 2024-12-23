

import cv2
import numpy as np
import pygame
import gui
import os
import pandas as pd
input_folder = "/Users/maryamhabeb/Desktop/datasets/gun_ziad"
for filename in os.listdir(input_folder):
        
    input_path = os.path.join(input_folder, filename)

    image = cv2.imread(input_path)

    print(image.shape)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)  
    print(image.shape)