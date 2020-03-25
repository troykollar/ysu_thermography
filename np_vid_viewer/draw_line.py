import cv2
import numpy as np

def findline(image, maxpoint):
    adjacent = np.arange(-1, 2)
    tmpmin = 999999
    minpoint = maxpoint
    points  = []
    points.append(maxpoint)
    finished = False
    while(not finished):

        for i in range(adjacent.size):
            for z in range(adjacent.size):
                if minpoint[0]-adjacent[i] > (image.shape[0] - 1) or minpoint[1]-adjacent[z] > (image.shape[1] - 1):
                    finished = True
                    break
                else:
                    tmpPoint = (minpoint[0]-adjacent[i],minpoint[1]-adjacent[z])

                if int(image[tmpPoint]) == 174:
                    print("Stuck?...")
                    finished = True
                    break
                if int(image[tmpPoint]) < tmpmin:
                    tmpmin = int(image[tmpPoint])
                    minpoint = tmpPoint

        print(finished)
        points.append(minpoint)

    return points

def drawline(image, points):
    for i in range(len(points)-1):
        image = cv2.line(image, points[i], points[i+1], (0,0,0), 1)

    return image
