import sys
import cv2
import imutils
from tqdm import tqdm
from skimage.measure import compare_ssim

# Load the two input images
imageA = cv2.imread(sys.argv[1])
imageB = cv2.imread(sys.argv[2])

normA = cv2.normalize(imageA, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
normB = cv2.normalize(imageB, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
 
# Convert the images to grayscale
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# Calculate absolute difference
diff = cv2.absdiff(grayA, grayB)

# Threshold the difference image, followed by finding contours to
# Obtain the regions of the two input images that differ
thresh = cv2.adaptiveThreshold(diff, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# List to store the bounding boxes
bboxes = []
# Loop over the contours and compute the bounding box of the 
# contour and then draw the bounding box on both input images 
# to represent where the two images differ. bounding_box is 
# a tuple of (x, y, w, h).
[bboxes.append(list(cv2.boundingRect(c))) for c in tqdm(cnts)]
bounding_boxes, _ = cv2.groupRectangles(bboxes[:-1], 1, eps=0.7)
# Loop of the bounding boxes and draw them
for box in tqdm(bounding_boxes):
	# Unpack the x, y, w, h values
	x, y, w, h = tuple(box)
	# Draw the bounding boxes
	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 6)
	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 6)

# show the output images
cv2.imwrite("Original.jpg", imageA)
cv2.imwrite("Modified.jpg", imageB)
cv2.imwrite("Diff.jpg", diff)
cv2.imwrite("Thresh.jpg", thresh)