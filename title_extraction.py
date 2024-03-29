#-*- coding:utf-8 -*-
try:
	from PIL import Image
except ImportError:
	import Image
import pytesseract
import cv2
import numpy as np
import math
from pythonRLSA import rlsa

def title_extraction(filepath):
	img = cv2.imread(filepath + '/0.jpg') # reading the image
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert2grayscale
	(thresh, binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # convert2binary
	### cv2.imwrite(filepath + filename + '-binary.png', binary)

	contours, _ = cv2.findContours(~binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours

	for contour in contours:
		# draw on rectangle around those contours on main image
		[x, y, w, h] = cv2.boundingRect(contour)
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)

	mask = np.ones(img.shape[:2], dtype="uint8") * 255 # create blank image of same dimension of the original image

	contours, _ = cv2.findContours(~binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	heights = [cv2.boundingRect(contour)[3] for contour in contours] # collecting heights of each contours

	avgheight = sum(heights) / len(heights) # average height

	# finding the larger contours
	# Applying Height heuristic
	for c in contours:
		[x, y, w, h] = cv2.boundingRect(c)
		if h > 1.5 * avgheight:
			cv2.drawContours(mask, [c], -1, 0, -1)

	x, y = mask.shape

	value = max(math.ceil(x/100), math.ceil(y/100)) + 20 # heuristic
	mask = rlsa.rlsa(mask, True, False, value) # rlsa application

	contours, _ = cv2.findContours(~mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours

	mask2 = np.ones(img.shape, dtype="uint8") * 255 # blank 3 layer image

	for contour in contours:
		[x, y, w, h] = cv2.boundingRect(contour)
		if w > 0.35 * img.shape[1]: # width heuristic applied
			title = img[y:y+h, x:x+w]
			mask2[y:y+h, x:x+w] = title # copied title contour onto the blank image

	for i in range(mask2.shape[0]):
		for j in range(mask2.shape[1]):
			if mask2[i,j,0] != mask2[i,j,1]:
				mask2[i,j,0] = mask2[i,j,2] = mask2[i,j,1]

	cv2.imwrite(filepath + '/title.png', mask2)
