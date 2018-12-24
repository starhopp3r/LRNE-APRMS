import sys
import cv2
import numpy as np
import imutils

# Lower bound for each channel
lower = (0, 0, 0)
# Upper bound for each channel
upper = (255, 255, 255)
# Read images
img1 = cv2.imread(sys.argv[1])
img2 = cv2.imread(sys.argv[2])
# Compute absolute difference
difference = cv2.absdiff(img1, img2)
# Convert to grayscale
mask = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
# Set threshold
threshold = int(sys.argv[3])
# Compute image mask
image_mask =  mask > threshold
# Create an empty canvas
canvas = np.zeros_like(img1, np.uint8)
# Overlay image mask on empty canvas
canvas[image_mask] = img1[image_mask]
# Create color mask
color_mask = cv2.inRange(canvas, lower, upper)
img1[color_mask != 0] = [0, 0, 255]
# Save the canvas
cv2.imwrite(sys.argv[4], img1)