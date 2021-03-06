[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FAntoineAndre%2Faruco_video_homography&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# A short script to detect and patch a video on an other

## About

This script is mainly made for educationnal purposes to explain the role of homography and its omnipresent place in commonly used image processing softwares.


![figureImg](aruco_detect_fridge3.gif)

This kind of patching is offently made seamlessly in softwares such as Adobe premiere or Adboe After Effects and these ones relie on subfunction calls to the openCV library. The goal of this repository is to present how heavy softwares use the patching method with a more pratical view which is the detection of corners (made with arUco markers) and the incrustation with an homography.

_Consider this script as the level 0 of the 3D incrustation and image processing_

**Note that the script needs the libraries numpy, openCV and aruco to work correctly.**

## Markers generation

The ArUco markers can be generated from this short script :

```
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

fig = plt.figure()
nx = 2
ny = 2
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict,i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

plt.savefig("markers.pdf")
plt.show()
```

Once this is done, the markers can be printed on a board (or any other support).

![markers](markers.png)

## How to use

The program comes with some small features such as the possibility to write an output file of the result or the possibility to use the camera of the laptop to detect the markers and patch the homography.

You have to change the number of your marker ids to respect the following order :

**top left, top right, bottom right, bottom left.**

furthermore, some lines of the script can be uncommented to provide a feedback to the user, such as the id number of the markers or their centers...

### 3rd party libraries

The used libraries can be downloaded and installed with the following pip commands:

- pip install numpy
- pip install opencv-python
- pip install aruco
- (optionnal : pip install matplotlib)