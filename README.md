# pywhycon ![Whycon tag with ID](whycon-code.jpg)

Python wrapper for Whycon.

### Whycon is precise, efficient and low-cost localization system 

_WhyCon_ is a version of a vision-based localization system that can be used with low-cost web cameras, and achieves millimiter precision with very high performance.
The system is capable of efficient real-time detection and precise position estimation of several circular markers in a video stream. 
It can be used both off-line, as a source of ground-truth for robotics experiments, or on-line as a component of robotic systems that require real-time, precise position estimation.
_WhyCon_ is meant as an alternative to widely used and expensive localization systems. It is fully open-source.
_WhyCon-orig_ is WhyCon's original, minimalistic version that was supposed to be ROS and openCV independent.

###<a name="whycon_core">Core library</a>
The package is a wrapper of the <a href="https://github.com/ivomarvan/whycon_core">Whycon core library</a>. 

**For citations of articles, contacts to the original author, please see these pages. You will also find citations of projects that contributed to the development of the Whycon.**
(This page is also part of this repository as a submodule and can be found as README.md in the whycon_core directory.)

### <a name="dependencies">Dependencies</a>

* <b>OpenCVcv</b>

###<a name="building">Building</a>

####Whycon core library

The Whycon core library is a submodule of this repository.

If you do not have a _whycon_core_ directory in the root directory, enter
`git submodule init`
`git submodule update`

If you do not have the whycon_core library installed, go to the whycon_coore directory 
and install it according to the README listed there.

TLDR:

`cd whycon_core`

something like `conda activate <your enviroment>`

`make USE_OPENCV_FROM_PYTHON=1`

`sudo make install`

