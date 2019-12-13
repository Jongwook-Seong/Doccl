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

	'''
	# find minimum width of images
	min_img_width = min(i.width for i in imgs)

	# find total height of all images
	total_height = 0
	for i, img in enumerate(imgs):
		total_height += imgs[i].height

	# create new image object with width and total height
	merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))

	# paste images together one by one
	y = 0
	for img in imgs:
		merged_image.paste(img, (0, y))
		y += img.height

	# save merged image
	merged_image.save(output_path + '.jpg')
	# save first page image
	imgs[0].save(output_path + '-p1.jpg')
	'''
	if not exists(output_path):
		os.mkdir(output_path)
	for i, img in enumerate(imgs):
		img.save(output_path + ('/{}.jpg' .format(i)))

	return output_path

#filename = 'Oliveira_Fast_CNN-Based_Document_ICCV_2017_paper.pdf'
#filename = 'vanBeusekom--DA--Document-Layout-Analysis.pdf'
#filename = 'Document_Structure_and_Layout_Analysis'
#filepath = '/home/sjw/Documents/Capstone2/pdf list/'
#temppath = './temp/'
#filelist = [f for f in os.listdir(filepath) if isfile(join(filepath, f))]
#for filename in filelist:
#	convert_pdf(filepath + filename, temppath + filename.split('.pdf')[0])
#convert_pdf('/home/sjw/Documents/pdf list/Oliveira_Fast_CNN-Based_Document_ICCV_2017_paper.pdf', './temp')
#convert_pdf('/home/sjw/Documents/Capstone2/pdf list/' + filename, './temp/' + filename.split('.pdf')[0])
