# Numpy Video Viewer

## Installation

The simplest installation of the package is using Git.

Within the directory of the project where you will be using the package, run the following commands:

If you are installing within a Git repository enter

```bash
git submodule add https://github.com/troykollar/np_vid_viewer
```

This is very similar to cloning the GitHub repository of the `np_vid_viewer` package, but since it is bad practice to have a Git repository within another, a submodule is created. This allows you to pull updates by simplying entering the directory of the package and using `git pull`.

If you are not using the package within a Git repository you can simply use:

```bash
git clone https://github.com/troykollar/np_vid_viewer
```

You can still download updates using `git pull`, however it is best not to use a Git repository within another unless it is a submodule.

## Usage

Once the `np_video_viewer` package is installed within your project directory. The package can be used by simply importing the package into your file. An example script is shown

```python
import np_vid_viewer

temp_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/thermal_cam_temps.npy"
merged_data_file = "/media/troy/TroyUSB/thermography/4-8_part_merged_data/4-8_part_merged_data/merged_data.npy"

VIEWER = np_vid_viewer.NpVidTool(temp_filename=temp_data_file,
                                 data_filename=merged_data_file,
                                 mp_data_on_vid=False,
                                 remove_top_reflection=False,
                                 remove_bottom_reflection=False)

VIEWER.play_video()
```

## NpVidTool Constructor

When creating an `NpVidTool` object, the constructor has 2 required arguments, `temp_filename` and `data_filename`. `temp_filename` is the location and filename of the thermal cam temperature data. `data_filename` is the location and filename of the merged data that is corresponding to the temperature data.

The other arguments of the constructor are:

`mp_data_on_vid` - Setting this to true will overlay the meltpool data overtop of the video. This can be difficult to see on very small datasets, since the font size is proportional to the size of the frame.

`remove_top_reflection` - Settting this to true will attempt to remove the reflection of the laser head above the piece.

`remove_bottom_reflection` - Setting this to true will attempt to remove the reflection of heat on the base underneath the piece. On certain datasets this can cause the program not to run because it may not be able to locate the lower bounds of the piece and crash. This issue is being looked into.

## Functions

The function used in this example is `play_video(waitKey=1)`. This will simply generate and play the video of the thermal camera based on the arguments specified in the constructor (`mp_data_on_vid`, `remove_top_reflection`, `remove_bottom_reflection`). The argument `waitKey` is the number of milliseconds of delay between when each frame is shown. It must be an integer greater than 1.

The other functions that can be used from the VIEWER class are:

`save_video(playback_speed=15, realtime_framerate=4)`

- `playback_speed` represents the speed the video will be played relative to the realtime framerate the video was taken at. This defaults to 15, since the default realtime framerate is 4. Giving a video at 60 fps.
- `realtime_framerate` is the realtime framerate the video was recorded at. This defaults to 4 (the current realtime framerate of the data available)

`generate_threshold_image(threshold=800)`

- `threshold` is the temperature threshold that a pixel must reach to be incremented in the threshold image.

`save_hotspot_video(playback_speed=15, realtime_framerate=4, save_img=False)`

- `playback_speed` represents the speed the video will be played relative to the realtime framerate the video was taken at. This defaults to 15, since the default realtime framerate is 4. Giving a video at 60 fps.
- `realtime_framerate` is the realtime framerate the video was recorded at. This defaults to 4 (the current realtime framerate of the data available)
- `save_img` is a boolean that will tell the function to save the final image of the hotspot video as .png