# pywhycon ![Whycon tag with ID](./whycon-code.jpg)

Python wrapper for Whycon.

### Whycon is precise, efficient and low-cost localization system 

_WhyCon_ is a version of a vision-based localization system that can be used with low-cost web cameras, and achieves millimiter precision with very high performance.
The system is capable of efficient real-time detection and precise position estimation of several circular markers in a video stream. 
It can be used both off-line, as a source of ground-truth for robotics experiments, or on-line as a component of robotic systems that require real-time, precise position estimation.
_WhyCon_ is meant as an alternative to widely used and expensive localization systems. It is fully open-source.
_WhyCon-orig_ is WhyCon's original, minimalistic version that was supposed to be ROS and openCV independent.


### <a name="dependencies">Dependencies</a>

* <b>OpenCV</b>
* <b>Whycon Core library</b> - see bellow
* <b>pkconfig</b> - only for module building
* <b>pybind11</b> - only for module building
* <b>numpy</b>

### <a name="install">Install</a>

You have to install the package from your **active python environment**.

Depending on your environment, you may need to enter something like

`conda activate _your_python_environment_name_` 

or 

`workon _your_python_environment_name_`.


#### Makefile

Compile and linking module to **./bin/whycon.so**.

(It also compiles the _Whycon Core library_.)

    make

#### setup.py

    ./setup.py install

(It calls the make [see above] and installs the whycon package in the current python environment.)


#### Pip

    pip install whycon

## Examples

Examples are in the _usecases_ directory in the <a href="https://github.com/ivomarvan/pywhycon">repo on GitHub</a>.

#### show_help.py

It only tests that the module was installed successfully. It prints the help message of the module.

#### camera_test.py

Turn on the USB webcam and see what it sees. 
If Whycon-markers are found in the image, they will be highlighted 
and their found properties will be written to the console.

#### autocalibration_test.py

Automatic calibration of space transformation parameters by monitoring 
four WhyCon markers arranged in a square 
(with the configured length of its side).

###### web_camera.py  

Auxiliary object, camera abstraction.
(Searches for the first unshaded camera.)

###### window.py

Auxiliary object, Screen window abstraction.


#### Whycon core library as a submodule

The Whycon core library is a git submodule of this repository.

If you do not have a _whycon_core_ directory in the root directory, enter

    git submodule init
    git submodule update


### <a name="whycon_core">Whycon Core library</a>
The package (pywhycon) is a wrapper of the <a href="https://github.com/ivomarvan/whycon_core">Whycon core library</a>. 

**For citations of articles, contacts to the original author, please see these pages. You will also find citations of projects that contributed to the development of the Whycon.**

<hr>

