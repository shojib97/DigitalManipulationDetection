import os
import cv2
import tqdm
import numpy as np



def NoiseLevelAnalysis(Image, FilterSize, NoiseAmplitude):
    # creating median filtered image
    MedianFilteredImage = cv2.medianBlur(Image,FilterSize)

    # Getting the diff image
    diffImage = NoiseAmplitude * cv2.absdiff(Image, MedianFilteredImage)
    
    return diffImage



if __name__ == "__main__":
    InputImagePath = "japan_tower.png"

    # Checking if image exists
    if not os.path.exists(InputImagePath):
        print("Input Image not found.")
        exit(1)

    # Reading the image in BGR format
    Image = cv2.imread(InputImagePath)

    # Calling the main algorthm to do copy-move-detection
    NoiseLevelImage = NoiseLevelAnalysis(Image, 3, 2)

    cv2.imshow("NoiseLevelAnalysis", NoiseLevelImage)
    cv2.waitKey(0)