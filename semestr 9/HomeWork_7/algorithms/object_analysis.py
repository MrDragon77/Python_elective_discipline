"""
Шаблонный метод (Template method)
"""
import cv2
import numpy as np
import random

class ObjectAnalysis(object):
    def template_method(self, image):

        image = self.noise_filtering(image)
        data = self.segmentation(image)
        data = self.object_parameters(data)

        return data

    def noise_filtering(self, image):
        raise NotImplementedError()

    def segmentation(self, data):
        raise NotImplementedError()

    def object_parameters(self, data):
        (image, data) = data
        (numLabels, labels, stats, centroids) = data
        x = []
        y = []
        w = []
        h = []
        area = []
        for i in range(1, numLabels):
            # extract the connected component statistics for the current
            # label
            x.append(stats[i, cv2.CC_STAT_LEFT])
            y.append(stats[i, cv2.CC_STAT_TOP])
            w.append(stats[i, cv2.CC_STAT_WIDTH])
            h.append(stats[i, cv2.CC_STAT_HEIGHT])
            area.append(stats[i, cv2.CC_STAT_AREA])

        return (x, y, w, h, area)


class BinaryImage(ObjectAnalysis):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        median = cv2.medianBlur(image, 5)
        return median

    def segmentation(self, image):
        output = cv2.connectedComponentsWithStats(
            image,
            4, # connectivity
            cv2.CV_32S)
        return (image, output)

class MonochromeImage(BinaryImage):
    def __init__(self):
        pass

    def noise_filtering(self, image):
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred

    def segmentation(self, image):
        edges = cv2.Canny(image,100,200)
        # cv2.imshow('Canny edges', edges)
        # cv2.waitKey(0)
        output = cv2.connectedComponentsWithStats(
            edges,
            4,  # connectivity
            cv2.CV_32S)
        return (image, output)

class ColorImage(MonochromeImage):
    def __init__(self):
        pass

    def segmentation(self, image):
        src = image
        cv2.imshow('Source Image', src)

        kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
 
        imgLaplacian = cv2.filter2D(src, cv2.CV_32F, kernel)
        sharp = np.float32(src)
        imgResult = sharp - imgLaplacian

        imgResult = np.clip(imgResult, 0, 255)
        imgResult = imgResult.astype('uint8')
        imgLaplacian = np.clip(imgLaplacian, 0, 255)
        imgLaplacian = np.uint8(imgLaplacian)
 
        # cv2.imshow('Laplace Filtered Image', imgLaplacian)
        # cv2.imshow('New Sharped Image', imgResult)

        bw = cv2.cvtColor(imgResult, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # cv2.imshow('Binary Image', bw)

        dist = cv2.distanceTransform(bw, cv2.DIST_L2, 3)
 
        cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
        # cv2.imshow('Distance Transform Image', dist)

        _, dist = cv2.threshold(dist, 0.4, 1.0, cv2.THRESH_BINARY)
 
        kernel1 = np.ones((3,3), dtype=np.uint8)
        dist = cv2.dilate(dist, kernel1)
        # cv2.imshow('Peaks', dist)

        dist_8u = dist.astype('uint8')

        contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
        markers = np.zeros(dist.shape, dtype=np.int32)

        for i in range(len(contours)):
            cv2.drawContours(markers, contours, i, (i+1), -1)
 
        cv2.circle(markers, (5,5), 3, (255,255,255), -1)
        markers_8u = (markers * 10).astype('uint8')
        # cv2.imshow('Markers', markers_8u)

        cv2.watershed(imgResult, markers)
 
        mark = markers.astype('uint8')
        mark = cv2.bitwise_not(mark)
        # cv2.imshow('Markers', mark)

        # colors = []
        # for contour in contours:
        #     colors.append((random.randint(0,256), random.randint(0,256), random.randint(0,256)))
 
        # dst = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)

        # for i in range(markers.shape[0]):
        #     for j in range(markers.shape[1]):
        #         index = markers[i,j]
        #         if index > 0 and index <= len(contours):
        #             dst[i,j,:] = colors[index-1]

        # cv2.imshow('Final Result', dst)
        # cv2.waitKey(0)

        output = cv2.connectedComponentsWithStats(
            mark,
            4,  # connectivity
            cv2.CV_32S)
        return (image, output)

"""
Декоратор - структурный паттерн
"""

class FilteredAnalysis(ObjectAnalysis):
    def __init__(self, obj):
        self._proc = obj

    def template_method(self, image):
        (_x, _y, _w, _h, _area) = self._proc.template_method(image)
        x = []
        y = []
        w = []
        h = []
        area = []

        for i in range(len(_area)):
            if _area[i] > 10 and _area[i] < 2500:
                x.append(_x[i])
                y.append(_y[i])
                w.append(_w[i])
                h.append(_h[i])
                area.append(_area[i])

        return (x,y,w,h,area)

class HuMomentsAnalysis(ObjectAnalysis):
    def __init__(self, obj, image_for_contours=None):
        self._proc = obj
        self._image_for_contours = image_for_contours

    def template_method(self, image):
        self._image_for_contours = image
        
        (_x, _y, _w, _h, _area) = self._proc.template_method(image)
        
        x = []
        y = []
        w = []
        h = []
        area = []
        hu_moments = []

        for i in range(len(_area)):
            x.append(_x[i])
            y.append(_y[i])
            w.append(_w[i])
            h.append(_h[i])
            area.append(_area[i])

            hu = self._compute_hu_moments_for_object(i, _x[i], _y[i], _w[i], _h[i])
            hu_moments.append(hu)
        
        return (x, y, w, h, area, hu_moments)
    
    def _compute_hu_moments_for_object(self, obj_index, x, y, w, h):
        x1 = max(0, x - 2)
        y1 = max(0, y - 2)
        x2 = min(self._image_for_contours.shape[1], x + w + 2)
        y2 = min(self._image_for_contours.shape[0], y + h + 2)
        roi = self._image_for_contours[y1:y2, x1:x2].copy()

        if len(roi.shape) == 3:
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        else:
            roi_gray = roi
        
        _, binary = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       
        if len(contours) == 0:
            return np.zeros(7)
        
        largest_contour = max(contours, key=cv2.contourArea)
        
        moments = cv2.moments(largest_contour)
        hu_moments = cv2.HuMoments(moments)
        hu_moments = hu_moments.flatten()
        hu_moments = np.array([-np.sign(x) * np.log10(np.abs(x) + 1e-10) for x in hu_moments])
        
        return hu_moments

if __name__== '__main__':
    print("Binary Image Processing")
    bin_segm = BinaryImage()
    (x,y,w,h,area) = bin_segm.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])
            
    print("Monochrome Image Processing")
    mono_segm = MonochromeImage()
    (x,y,w,h,area) = mono_segm.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])
            
    print("Color Image Processing")
    color_segm = ColorImage()
    (x,y,w,h,area) = color_segm.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_COLOR))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])

    print("Decorated Binary Image Processing")
    filt_bin = FilteredAnalysis(BinaryImage())
    (x, y, w, h, area) = filt_bin.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_GRAYSCALE))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i]])
            
    print("Decorated Image Hu Moments Processing")
    hu_moments = HuMomentsAnalysis(ColorImage())
    (x, y, w, h, area, hu_moments) = hu_moments.template_method(cv2.imread('./data/1.jpg', cv2.IMREAD_COLOR))
    for i in range(len(area)):
            print([x[i], y[i], w[i],h[i],area[i], str(hu_moments[i])])
            

