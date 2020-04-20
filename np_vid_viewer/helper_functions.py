import cv2
import numpy as np
import np_vid_viewer


def min_scale_factor(data_frame):
    """Given a frame of data, returns the minimum scale factor for the image to be at least 240x320"""
    height = data_frame.shape[0]
    width = data_frame.shape[1]

    scale_factor = 1
    while height * scale_factor < 240 or width * scale_factor < 320:
        scale_factor += 1

    return scale_factor


def get_build_folder(temp_filename: str):
    build_folder = temp_filename[:temp_filename.rfind('/')]
    return build_folder


def get_build_number(temp_filename: str):
    build_folder = get_build_folder(temp_filename)
    build_number = build_folder[:build_folder.find('_')]
    build_number = build_number[(build_number.rfind('/') + 1):]
    return build_number


def get_build_folder_name(temp_filename: str):
    build_folder = get_build_folder(temp_filename)
    build_folder_name = build_folder[:build_folder.rfind('/')]
    build_folder_name = build_folder_name[build_folder_name.rfind('/') + 1:]
    return build_folder_name


def get_follow_meltpool_cords(frame, follow_size):
    max_temp = np.amax(frame)
    max_temp_y = np.where(frame == max_temp)[0][0]
    max_temp_x = np.where(frame == max_temp)[1][0]

    if max_temp_x < follow_size:
        left_x = 0
        right_x = follow_size * 2
    elif max_temp_x > frame.shape[1] - follow_size:
        right_x = frame.shape[1]
        left_x = right_x - (follow_size * 2)
    else:
        left_x = max_temp_x - follow_size
        right_x = max_temp_x + follow_size

    if max_temp_y < follow_size:
        top_y = 0
        bottom_y = follow_size * 2
    elif max_temp_y > frame.shape[0] - follow_size:
        bottom_y = frame.shape[0]
        top_y = frame.shape[0] - (follow_size * 2)
    else:
        top_y = max_temp_y - follow_size
        bottom_y = max_temp_y + follow_size

    return top_y, bottom_y, left_x, right_x


def add_white_border_on_img(img):
    img_height = img.shape[0]

    # Add white border on top of img
    img = cv2.copyMakeBorder(img,
                             int(img_height * (7 / 16)),
                             0,
                             0,
                             0,
                             cv2.BORDER_CONSTANT,
                             value=(255, 255, 255))
    return img


def get_follow_contour_cords(frame, follow_size, cog_x, cog_y):
    if cog_x < follow_size:
        left_x = 0
        right_x = follow_size * 2
    elif cog_x > frame.shape[1] - follow_size:
        right_x = frame.shape[1]
        left_x = right_x - (follow_size * 2)
    else:
        left_x = cog_x - follow_size
        right_x = cog_x + follow_size

    if cog_y < follow_size:
        top_y = 0
        bottom_y = follow_size * 2
    elif cog_y > frame.shape[0] - follow_size:
        bottom_y = frame.shape[0]
        top_y = frame.shape[0] - (follow_size * 2)
    else:
        top_y = cog_y - follow_size
        bottom_y = cog_y + follow_size

    return top_y, bottom_y, left_x, right_x