import plot
import numpy as np

plotting = plot.Plots(np.load('/home/rjyarwood/Documents/Research/ResearchData/4-8_part_merged_data/thermal_cam_temps'
                              '.npy', allow_pickle=True, mmap_mode='r'),
                      pixel=(5, 20),
                      threshold=500)
plotting.plotBubble()
