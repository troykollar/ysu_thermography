import cv2
from Visualization_script import get_visualization
from np_vid_viewer.helper_functions import printProgressBar

x_locations = []
y_locations = []
redraw = True


def on_click(event, x, y, flags, param):
    x_loc = x
    y_loc = y
    if event == cv2.EVENT_LBUTTONDOWN:
        x_locations.append(x_loc)
        y_locations.append(y_loc)
        img1[y_loc][x_loc] = [255, 255, 255]
        redraw = True


img1 = cv2.imread("/home/troy/Pictures/4-20_700.png")

window_name = "4-20"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, on_click)

while True:
    cv2.imshow(window_name, img1)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

cv2.destroyAllWindows()

path = '/media/troy/TroyUSB/thermography/All/Thermal Camera'
x_file = open('x_locations.txt', 'w')
y_file = open('y_locations.txt', 'w')
for x, y in zip(x_locations, y_locations):
    x_file.write(str(x) + '\n')
    y_file.write(str(y) + '\n')

x_file.close()
y_file.close()

for x, y in zip(x_locations, y_locations):
    get_visualization(path, x, y, end=27000)

print(x_locations)
print(y_locations)