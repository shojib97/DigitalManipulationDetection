import os
import cv2
import numpy as np



def ErrorLevelAnalysis(Image, Quality, Scale):
    # Write input image at specified jpg compression quality
    cv2.imwrite("CompressedImage_ErrorLevelAnalysis.jpg", Image, [cv2.IMWRITE_JPEG_QUALITY, Quality])

    # Reading compressed image
    CompressedImage = cv2.imread("CompressedImage_ErrorLevelAnalysis.jpg")

    # Getting absolute difference between Image and CompressedImage and multiply by Scale
    DiffImg = Scale * cv2.absdiff(Image, CompressedImage)

    return DiffImg


if __name__ == "__main__":
    InputImagePath = "japan_tower.png"

    # Checking if image exists
    if not os.path.exists(InputImagePath):
        print("Input Image not found.")
        exit(1)

    # Reading the image in BGR format
    Image = cv2.imread(InputImagePath)

    # Calling the main algorthm to do copy-move-detection
    ErrorLevelImage = ErrorLevelAnalysis(Image, 95, 15)

    cv2.imshow("ErrorLevelAnalysis", ErrorLevelImage)
    cv2.waitKey(0)