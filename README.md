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
                                 mp_data_on_vid=True,
                                 remove_top_reflection=True,
                                 remove_bottom_reflection=True)

VIEWER.play_video()
```
