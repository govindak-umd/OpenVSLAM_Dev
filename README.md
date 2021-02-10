# OpenVSLAM_Dev


## System:

The below code is tested on 

 - Ubuntu 18.05 LTS
 - NVIDIA GTX 950M
 
## Initial Installation

Do initial installation as per [this](https://openvslam.readthedocs.io/en/master/installation.html#subsection-common-linux-macos).

For Linux, the commands are all laid out here:

## Running on any dataset:

There are many sample datasets as seen [here](https://openvslam.readthedocs.io/en/master/simple_tutorial.html).
To extract any one specific folder in openvslam/build, do the following

 - Right click on the scenario and copy link
 - Copy the FILE_ID part of the link.
 
 For example, while trying to extract for aist_factory_A.zip, the link is 
 
    https://drive.google.com/file/d/10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0/view?usp=sharing
    
 Here the FILE_ID is 

    10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0
    
Now, to download and unzip anything from this directory, execute the following commands:

    $ FILE_ID="10JZjmZYntdpiDvIxe8sxLlF4xZ0exyw0"

    $ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null

    $ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"

    $ curl -sLb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o aist_factory_A.zip

    $ unzip aist_factory_A.zip 

You can see the extracted folder in the build directory now.
