import numpy as np
import cv2

img = cv2.imread("greysnake26x26.png", cv.IMREAD_GRAYSCALE) # The image pixels have range [0, 255]
img //= 255  # Now the pixels have range [0, 1]
img_list = img.tolist() # We have a list of lists of pixels

result = ""
for row in img_list:
    row_str = [str(p) for p in row]
    result += "[" + ", ".join(row_str) + "],\n"
