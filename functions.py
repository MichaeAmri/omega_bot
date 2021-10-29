import cv2 as cv
import numpy as np

def canny(img):
	img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
	blur = cv.GaussianBlur(img, (5, 5), 0)
	return cv.Canny(blur, 40, 200)		# 1 to 2 or 1 to 3

def make_coordinates(image, line_parameters):
	slope, intercept = line_parameters
	#print('average slope: ', slope, '\t\taverage_intercept: ',intercept)
	y1 = image.shape[0]
	y2 = 0  #int(y1 * (4/5))
	x1 = int((y1 - intercept) / slope)
	x2 = int((y2 - intercept) / slope)
	return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
	left_fit = []
	right_fit = []

	sharp_right_fit = []
	sharp_left_fit = []

	all_slope = []
	all_intercept = []

	while lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line.reshape(4)
			parameters = np.polyfit((x1, x2), (y1, y2), 1)
			slope = parameters[0]
			intercept = parameters[1]

			all_slope.append(slope)
			all_intercept.append(slope)
			if slope < 0:
				left_fit.append((slope, intercept))
			else:
				right_fit.append((slope, intercept))
			all_intercept.append(intercept)

		average_slope = np.average(all_slope)
		average_intercept = np.average(all_intercept)

		if min(all_slope) < 0 and max(all_slope) > 0:
			print('correct', min(all_slope), max(all_slope))

			left_fit_average = np.average(left_fit, axis=0)
			right_fit_average = np.average(right_fit, axis=0)

			left_line = make_coordinates(image, left_fit_average)
			right_line = make_coordinates(image, right_fit_average)

			return np.array([left_line, right_line])

		else:
			intercept_limit = np.average(all_intercept)
			for fit in (left_fit + right_fit):
				if fit[1] < intercept_limit:
					sharp_right_fit.append(fit)
				else:
					sharp_left_fit.append(fit)

			left_fit_average = np.average(sharp_left_fit, axis=0)
			right_fit_average = np.average(sharp_right_fit, axis=0)

			left_line = make_coordinates(image, left_fit_average)
			right_line = make_coordinates(image, right_fit_average)

			return np.array([left_line, right_line])


'''			all_slope.append(parameters[0])
			all_intercept.append(parameters[1])

			slope_limit = np.average(all_slope)
			intercept_limit = np.average(all_intercept)

		if min(all_slope) < 0 and max(all_slope) > 0:
			for i in range(len(all_slope)):
				if slope[i] < 0:
					left_fit.append((slope[i], intercept[i]))
				else:
					right_fit.append((slope[i], intercept[i]))
		else:
			for i in range(len(all_slope)):
				if intercept[i] < intercept_limit:
					left_fit.append((slope[i], intercept[i]))
				else:
					right_fit.append((slope[i], intercept[i]))
'''

def display_lines(image, lines):
	line_image = np.zeros_like(image)
	height = image.shape[0]
	width = image.shape[1]
	if lines is not None:
		for x1, y1, x2, y2 in lines:
			cv.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 8)
	cv.line(line_image, (width//2, 0), (width//2, height), (255, 255, 0), 4)
	return line_image

def mask(image):
	height = image.shape[0]
	width = image.shape[1]
	polygons = np.array([(0, height), (width, height), (9 * width / 10, 3 * height / 5), (1 * width / 10, 3 * height / 5)])
	mask = np.zeros_like(image)
	cv.fillPoly(mask, np.array([polygons], dtype=np.int64), 1024)
	masked_image = cv.bitwise_and(image, mask)
	return masked_image
