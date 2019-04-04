import cv2 as cv
import numpy as np
from typing import Tuple, List

kernel_length_factor = 25
kernel_width = 1
def _morph_open_and_find_contours(img: np.ndarray, kernel_size: Tuple[int, int]):
		open_kernel = cv.getStructuringElement(cv.MORPH_RECT, kernel_size)
		opened_img = cv.morphologyEx(img, cv.MORPH_OPEN, open_kernel)
		#copy = opened_img.copy()
		#contours, _ = cv.findContours(opened_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		contours, _ = cv.findContours(opened_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE ) 
		#cv.drawContours(copy, contours, -1, (0,255,0), 3)


		return opened_img, contours

def get_horizontal_and_vertical_contours(img , kernel_length_factor, kernel_width):
		kernel_length_factor = 20
		kernel_length_factor = 20
		kernel_size = ( int(img.shape[1] / kernel_length_factor), kernel_width )
		print(kernel_size)
		horizontal, hor_contours = _morph_open_and_find_contours(img, kernel_size )

		kernel_length_factor = 20
		kernel_length_factor = 20
		kernel_size = ( kernel_width, int(img.shape[0] / kernel_length_factor) )
		print("kernel_size--->", kernel_size)
		vertical, ver_contours	 = _morph_open_and_find_contours(img, kernel_size)

		return [horizontal, hor_contours, vertical, ver_contours]


def write_image(name, img, countours=None):
		#name = "/Users/shravanc/Desktop/working/" + name
		if countours is not None:
				new_copy = img.copy()
				cv.imwrite(name, new_copy)
		else:
				new_copy = img.copy()
				cv.imwrite(name, img)

def extract_tables(image_path: str):
		print("FINDING_BOUNDARY")
		orig = cv.imread(image_path)
		image = orig.copy()
		if image is None:
				raise AssertionError('Error opening image: ' + image_path)

		kernel = np.ones((15, 15), np.uint8)
		image = cv.dilate(image, kernel, iterations=1)

		#write_image('dilated_image.jpg', image)
		# gray covertion

		gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
		#write_image('gray.jpg', image)

		# apply thresholding
		#_, thresholded_inverted_image = cv.threshold(gray_image, 127, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
		_, thresholded_inverted_image = cv.threshold(gray_image, 175, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
		#write_image('thresholded_inverted.jpg', thresholded_inverted_image)

		horizontal, hor_contours, vertical, ver_contours = get_horizontal_and_vertical_contours(thresholded_inverted_image, kernel_length_factor, kernel_width)
		print("get_horizontal_and_vertical_contours")
		lines_img = vertical + horizontal
		lines_img = cv.morphologyEx(lines_img, cv.MORPH_CLOSE, np.full((10, 10), 255, dtype=np.uint8))

		lines_contours, lines_contour_hierarchy = cv.findContours(lines_img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

		# Remove all contours that have no parents(h[3]). This will give all level 1 contours.
		parent_contours = [c for c, h in zip(lines_contours, lines_contour_hierarchy[0].tolist()) if h[3] == -1]

		rects = []
		parent_contours = lines_contours
		print(image.shape)
		co_ordinates = [{'x':1, 'y':1, 'w': image.shape[1], 'h': image.shape[0]}]
		max_area = 0
		min_area = image.shape[1] * image.shape[0]
		flag = True
		extra_weight = 0
		for i, contour in enumerate(parent_contours):
				x, y, w, h = cv.boundingRect(cv.approxPolyDP(contour, 3, True))
				print(f"'x': {x}, 'y': {y},'w': {w},'h': {h}")
				if (w * h) / (image.shape[0] * image.shape[1]) > 0.3:
						print(f"'x': {x}, 'y': {y},'w': {w},'h': {h}")
						if (x * y) > max_area:
								max_area = x * y
								flag = False
								#co_ordinates[0] = {'x': x, 'y': y, 'w': w, 'h': h}
								co_ordinates[0] = {'x': x + extra_weight, 'y': y + extra_weight, 'w': w - extra_weight, 'h': h - extra_weight}

						if (x * y) < min_area:
								print("Hello Inside Here")
								min_area = x * y
								co_ordinates[0] = {'x': x + extra_weight, 'y': y + extra_weight, 'w': w - extra_weight, 'h': h - extra_weight}
								min_val = co_ordinates[0]


						pass

		print(f"FLAG----{flag}")

		if flag:
				kernel = np.ones((20, 20), np.uint8)
				img = cv.imread( image_path, cv.IMREAD_GRAYSCALE)
				_, binary = cv.threshold(img, 175, 255, cv.THRESH_BINARY_INV)
				binary = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

				contours, hierarcy = cv.findContours(binary, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
				parent_contours = [c for c, h in zip(contours, hierarcy[0].tolist()) if h[3] != -1]

				extra_weight = 60
				correction_factor = 2
				for contour in parent_contours:
						x, y, w, h = cv.boundingRect(cv.approxPolyDP(contour, 3, True))
						if (w * h) / (img.shape[0] * img.shape[1]) > 0.4:
								co_ordinates[0] = {'x': x + extra_weight, 'y': y + extra_weight, 'w': w - (extra_weight*correction_factor), 'h': h - (extra_weight*correction_factor)}

				


		print("=======================")
		print(co_ordinates)
		return orig, co_ordinates[0]
		#return image, co_ordinates[0]

def crop_image(image, top_left, bottom_right):
		"""
		Takes a numpy.ndarray and crop it to the given dimensions
		:param image: numpy.ndarray representing the image
		:param top_left: a tuple of the form (x, y)
		:param bottom_right: a tuple of the form (x, y)
		:return: a cropped image represented by a numpy.ndarray cropped to the given dimensions
		"""

		x1, y1 = top_left
		x2, y2 = bottom_right

		return image[y1:y2 + 1, x1:x2 + 1]


def crop_boundary(image_path):
		image, ordinates = extract_tables(image_path)
		cropped_image = crop_image(image, ((ordinates['x']), ordinates['y']), ((ordinates['x']+ordinates['w'] ), (ordinates['y'] + ordinates['h']))		)
		#write_image('cropped_image.jpg', cropped_image)
		write_image( image_path, cropped_image)
		print("========================cropped_image========================")


#image_path = "/Users/shravanc/Desktop/CPA_files/pending_files/pending_dup/image/1.jpg"
#image_path = "/Users/shravanc/Desktop/orig_636700872805155406_auditriskassessmentthedosanddontspart2-1.jpg"
#crop_boundary(image_path)
