"""Utility to remove the heat reflection from an image"""
import numpy as np

#TODO: Remove side reflections


def remove_top(img,
               distance=0,
               min_value=174,
               max_temp_threshold=1900,
               zero_level_threshold=176):
    """Set values above the hottest point to min_value to remove the reflection of heat.
        
    Parameters
    ----------
        img : np.ndarray
            img to remove reflection from
        distance : int
            number of pixels above the hottest point to draw until (default 0)
        min_value : int
            minimum value read from the thermal camera (default 174)
        max_temp_threshold : int
            the hotpoint must be greater than to continue removing reflections this is useful
            to prevent removing parts of the image during cooling
        zero_level_threshold : int
            lines that have an average value above `zero_level_threshold` will not be removed
    """
    max_value = np.amax(img)
    max_value_location = np.where(img == max_value)

    if max_value > max_temp_threshold:
        remove_to = max_value_location[0][0]
        while np.mean(img[remove_to - distance]) > zero_level_threshold:
            if remove_to < 1:
                print("Problem removing reflection.")
                break
            else:
                remove_to = remove_to - 1

        for i in range(0, remove_to - distance):
            img[i] = min_value


def remove_bottom(img, temp_data, min_value=174):
    lower_bounds = find_lower_bounds(temp_data)
    for i in range(0, len(lower_bounds)):
        x = lower_bounds[i][0]
        y = lower_bounds[i][1]
        img[y:, x] = min_value
        if i == 0:
            img[y:, :x] = min_value
        elif i == len(lower_bounds) - 1:
            img[y:, x:] = min_value


def find_lower_bounds(temp_data):
    """Find the lower bounds of the piece.

        Returns
        -------
        max_locations
            List of the first points at the zero level below the each max temp.
        """
    temp_data
    i = 0
    # Find the x and y value of the max temp of first frame
    max_x = np.where(temp_data[0] == np.amax(temp_data[0]))[1][0]
    max_y = np.where(temp_data[0] == np.amax(temp_data[0]))[0][0]

    # Find the x value of the max temp of the next frame
    next_max_x = np.where(temp_data[1] == np.amax(temp_data[1]))[1][0]

    # Create lists of the x and y values of the max temperatures
    max_x_locations = []
    max_y_locations = []

    # While the laser is moving to the right. (i.e. the next location > current location)
    while max_x < next_max_x:
        max_x_locations.append([i, max_x])
        max_y_locations.append([i, max_y])
        i = i + 1
        max_x = np.where(temp_data[i] == np.amax(temp_data[i]))[1][0]
        next_max_x = np.where(temp_data[i + 1] == np.amax(temp_data[i +
                                                                    1]))[1][0]
        max_y = np.where(temp_data[i] == np.amax(temp_data[i]))[0][0]

    for frame in range(0, len(max_y_locations)):
        while temp_data[frame, max_y_locations[frame][1],
                        max_x_locations[frame][1]] > 174:
            max_y_locations[frame][1] += 1

    max_locations = []
    j = 0
    for i in range(max_x_locations[0][1], max_x_locations[-1][1]):
        if i > max_x_locations[j][1]:
            j = j + 1
        max_locations.append((i, max_y_locations[j][1]))
    return max_locations
