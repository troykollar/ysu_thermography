import cv2
import numpy as np


def findline(image, maxpoint):
    adjacent = np.arange(-1, 2)

    minpoint = maxpoint
    points = []
    points.append(maxpoint)
    finished = False
    while (not finished):
        tmpmin = 0

        for i in range(adjacent.size):
            # print("Horizontal")
            for z in range(adjacent.size):
                # print("Vertical")
                if minpoint[0] - adjacent[i] > (image.shape[0] - 1) or minpoint[1] - adjacent[z] > (image.shape[1] - 1):
                    finished = True
                    break
                else:
                    # print("tmpPoint")
                    tmpPoint = (minpoint[0] - adjacent[i], minpoint[1] - adjacent[z])

                if int(image[tmpPoint]) == 174:
                    # print("Stuck?...")
                    finished = True
                    break
                if int(image[tmpPoint]) > tmpmin and tmpPoint not in points:
                    tmpmin = int(image[tmpPoint])
                    # print(tmpmin)
                    minpoint = tmpPoint
                    if minpoint in points:
                        finished = True
                        break

        # print(finished)
        points.append(minpoint)

    return points


def drawline(image, points):
    for i in range(len(points) - 1):
        image = cv2.line(image, points[i], points[i + 1], (0, 0, 0), 1)

    return image