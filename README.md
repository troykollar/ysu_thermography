- [Installation](#installation)
- [Usage](#usage)
  - [Command Line](#command-line)
    - [Dataset](#dataset)
    - [Viewer](#viewer)
    - [Composite](#composite)
    - [Plots](#plots)

# Installation

The simplest installation of the package is using Git.

Clone the repository using:

```bash
git clone https://github.com/troykollar/ysu_thermography.git
```

Install required libraries using (it is recommended, but not neccesary to do this within a virtual environment):

```bash
pip install -r requirements.txt
```

# Usage

Nearly all of the functions of the software can be used through both the command line and the GUI.

## Command Line

### Dataset

The file containing functions relevant to the dataset itself is `dataset.py`. This file generally will not be used directly, but can be used to help debug, as it will show the simplest possible video of the dataset if called directly.

To see all the possible arguments of `dataset.py` use:

```bash
python3 dataset.py -h
```

The arguments that are related to the dataset are:

```bash
temp_data: required
    filename (and location) of thermal cam temps file.
mp_data: optional
    filename (and location) of merged data file.
top: optional
    0 or 1 specifying whether or not to remove top reflections.
bot: optional
    0 or 1 specifying whether or not to remove bottom reflections.
scale: optional
    int specifying the factor to scale frames by.
range: optional
    start,end specifying frame range to use in dataset.
```

These arguments are used for other files wherever they are relevant.

### Viewer

The viewer class has functions for playing and saving videos of the dataset and possible tranformations of the data, as well as the ability to save individual frames of the dataset.

To use the viewer, the `viewer.py` file will be used.

To see all the possible arguments of `viewer.py` use:

```bash
python3 viewer.py -h
```

The arguments that are related to the viewer are:

```bash
play: optional
    int specifying frame delay in ms to play the video using OpenCV.
save: optional
    int specifying the framerate to save the video in using OpenCV.
frame: optional
    int specifying a frame to save in 16 bit color using matplotlib.
contour: optional
    int specifying the threshold to use if drawing a contour.
follow: optional
    str specifying what to focus the frame on.
    follow = 'max' centers the frame on the max temperature.
    follow = 'contour' centers the frame on the center of gravity of the contour (if present).
fsize: optional
    int specifying the size of the window when following max temp or contour.
info: optional
    'mp' or 'contour' to display an info pane with relevant info above video.
```

These arguments are used for other files wherever they are relevant.

### Composite

The Composite class has functions for generating and saving composite images.

To use the composite class, the `composite.py` file will be used.

To see all the possible arguments of `composite.py` use:

```bash
python3 composite.py -h
```

The arguments that are related to `composite.py` are:

```bash
threshold: optional
    int specifying the threshold to be used for the composite image.
dst_folder: optional
    str specifying where to save the composite image. Defaults to build folder.
cap: optional
    int specifying the max number of frames to use for composite.
max: optional
    0 or 1 specifying whether or not to generate a max temperature composite image.
avg: optional
    0 or 1 specifying whether or not to generate an average temperature composite image.
int: optional
    int specifying threshold to be used to generate a temperature integration composite image.
hotspot: optional
    0 or 1 specifying whether or not to generate a hotspot composite image.
```

These arguments are used for other files wherever they are relevant.

### Plots

Command line functions related to plotting can be done using the `pixel_selector.py` file.

There are no arguments that relate directly to pixel_selector.py, but there are still other arguments needed (related to the dataset, and composite).

To see all the possible arguments of `pixel_selector.py` use:

```bash
python3 pixel_selector.py -h
```
