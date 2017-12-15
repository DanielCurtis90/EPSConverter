from __future__ import print_function
import ghostscript
import os, sys
from PIL import Image


def convert_to_png():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	input_extensions = ('.eps')

	for filename in os.listdir(os.path.join(dir_path, "tmp")):
		if str(filename).endswith(input_extensions):
			full_filename = os.path.join(os.path.join(dir_path, "tmp"),filename)
			im = Image.open(full_filename)
			pngim = im.convert('RGB')
			new_filename = os.path.splitext(filename)[0] + '.png'
			new_filename_address = dir_path + "\\tmp\\" + new_filename
			pngim.save(new_filename_address)
	return (new_filename, new_filename_address)

