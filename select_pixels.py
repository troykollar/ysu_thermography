import cv2
from Visualization_script import get_visualization
from bubble_plot_3d import plotBubble
from datetime import datetime

pixel_locations = []
corner_locations = []
redraw = True

select_corners = True


def on_click(event, x, y, flags, param):
    x_loc = x
    y_loc = y
    if event == cv2.EVENT_LBUTTONDOWN:
        if select_corners:
            corner_locations.append((x, y))
        else:
            pixel_locations.append((x, y))


img1 = cv2.imread("/home/troy/Pictures/4-20_700.png")

window_name = "4-20"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, on_click)

while True:
    if len(corner_locations) < 4:
        select_corners = True
    else:
        select_corners = False

    draw_img = img1.copy()

    for corner_pixel in corner_locations:
        corner_x = corner_pixel[0]
        corner_y = corner_pixel[1]
        draw_img[corner_y][corner_x] = [0, 255, 255]

    for pixel in pixel_locations:
        pixel_x = pixel[0]
        pixel_y = pixel[1]
        draw_img[pixel_y][pixel_x] = [255, 255, 255]

    cv2.imshow(window_name, draw_img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('z'):
        if len(pixel_locations) > 0:
            del pixel_locations[-1]
        elif len(corner_locations) > 0:
            del corner_locations[-1]
        else:
            pass

cv2.destroyAllWindows()

savetime = str(datetime.now().month) + '-' + str(
    datetime.now().day) + '_' + str(datetime.now().hour) + '-' + str(
        datetime.now().minute)

path = '/media/troy/TroyUSB/thermography/All/Thermal Camera'
temp_file = '/media/troy/TroyUSB/thermography/All/Thermal Camera/thermal_cam_temps.npy'
threshold = 200

if len(corner_locations) == 4:
    if len(pixel_locations) > 0:
        corner_locations.sort()
        pixel_locations.sort()
        loc_file = open('pixel_locations' + savetime + '.txt', 'w')
        loc_file.write('Corner locations:\n')
        for corner_pixel in corner_locations:
            loc_file.write(str(corner_pixel) + '\n')
        loc_file.write('\nSelected Pixels:\n')
        for pixel in pixel_locations:
            loc_file.write(str(pixel) + '\n')

        loc_file.close()

        for pixel in pixel_locations:
            pixel_x = pixel[0]
            pixel_y = pixel[1]
            print('\nGenerating 2D plots for: ' + str(pixel))
            get_visualization(path, pixel_x, pixel_y, threshold=threshold)
            print('\nGenerating 3D plot for: ' + str(pixel))
            plotBubble(temp_file, pixel, threshold=threshold)
