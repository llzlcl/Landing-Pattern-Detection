import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('C:\\Users\\lenovo\\1.png')
print img
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print img_gray
