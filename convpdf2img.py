import tempfile
import os
from os.path import exists, isfile, join
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf(file_path, output_path):
	# save temp image files in temp dir, delete them after we are finished
	with tempfile.TemporaryDirectory() as temp_dir:
		# convert pdf to multiple image
		images = convert_from_path(file_path, output_folder=temp_dir)

		# save images to temporary directory
		temp_images = []
		for i in range(len(images)):
			image_path = '{}/{}.jpg' .format(temp_dir, i)
			images[i].save(image_path, 'JPEG')
			temp_images.append(image_path)
			break

		# read images into pillow.Image
		imgs = list(map(Image.open, temp_images))

	if not exists(output_path):
		os.mkdir(output_path)
	for i, img in enumerate(imgs):
		img.save(output_path + ('/{}.jpg' .format(i)))

	return output_path
