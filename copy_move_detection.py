from sklearn.cluster import DBSCAN
import numpy as np
import cv2


class Detect(object):
	def __init__(self, image):
		self.image = image


	# Method for detection keypoints and descriptors
	def siftDetector(self):
		try:		# Function shifted to main library in the newer versions
			sift = cv2.SIFT_create()
		except:		# Else reading it from the contribution module
			sift = cv2.xfeatures2d.SIFT_create()
		
		# Converting image to grayscale and computing keypoints and descriptors.
		gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.key_points, self.descriptors = sift.detectAndCompute(gray, None)


	# Method for locating the forgery (copy-paste type)
	def locateForgery(self, eps, min_sample):
		# Getting the clusters by DBSCAL algorithm
		clusters = DBSCAN(eps=eps, min_samples=min_sample).fit(self.descriptors)
		size = np.unique(clusters.labels_).shape[0] - 1
		
		forgeryImage = self.image.copy()

		# If no cluster found - no forgery, return the input image
		if (size == 0) and (np.unique(clusters.labels_)[0] == -1):
			# print('No Forgery Found!!')
			return self.image

		if size == 0:
			size = 1

		cluster_list = [[] for i in range(size)]
		for idx in range(len(self.key_points)):
			if clusters.labels_[idx] != -1:
				cluster_list[clusters.labels_[idx]].append((int(self.key_points[idx].pt[0]), int(self.key_points[idx].pt[1])))

		for points in cluster_list:
			if len(points) > 1:
				for idx1 in range(1, len(points)):
					cv2.line(forgeryImage, points[0], points[idx1], (255, 0, 0), 1)

		return forgeryImage