import np_vid_viewer
import sys

temp_data_file = sys.argv[1]
print(temp_data_file)
merged_data_file = sys.argv[2]
print(merged_data_file)
display = sys.argv[3].lower() == 'true'
print(display )
top = sys.argv[4].lower() == 'true' 
print(top )
bottom = sys.argv[5].lower() == 'true' 
print(bottom )
delay = int(sys.argv[6])
print(delay )
scale = float(sys.argv[7])
print(scale )


VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
                                 mp_data_on_vid=display,
                                 scale_factor=scale,
                                 frame_delay=delay,
                                 remove_top_reflection=top,
                                 remove_bottom_reflection=bottom)

VIEWER.play_video()
