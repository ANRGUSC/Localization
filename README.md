# Localization
This repository maintains the localization software. The python version of the framework is available in "python-version" folder, while the GPU optimziation software is available inside the "GPU-Optimizations" folder.

Note:
-----

Please refer the architecture diagram in Section 8 of the report located in /root/GPU-Optimizations/GPU_Optimization_Report.pdf. This is to understand the various modules and their installing in the appropriate PCs. It is recommended to read through the section thoroughly before installing the required components


INSTALLATION:
--------------

Section 1: Location of files to run:
------------------------------------
1) Location of the python client code (to be installed in a PC that functions as the mqtt receiver end and posts the feed data to the GPU engine): /root/GPU-Optimizations/1080_Python_Client/mqtt-server.py

2) Location of the CPP + CUDA server code (Present in a device that contains an NVIDIA CUDA enabled GPU): /root/GPU-Optimizations/Jetson_CPP_Server
 
 
Section 2: Instructions to run:
-------------------------------
1) First start the server by logging into the Jetson board

2) Navigate to the server binary that will be generated in /root/GPU-Optimizations/Jetson_CPP_Server

3) Start executing the server program using the command format: ./server [port_number]

4) Edit the python client code in the eclipse pc with the server ip and the port number entered in step 1 (In this case, enter the IP address of the Jetson board)

5) Start the python client code and wait for incoming mqtt requests
 
 
Section 3: To edit thread Numbers or the GPU server code and recompile
----------------------------------------------------------------------
1) It is possible to change the parallel thread number by navigating to /root/GPU-Optimizations/Jetson_CPP_Server/server.cpp and line number: 82 by editing the variable numThr.

2) The compile command for the entire CPP and CUDA files is available in the file: /root/GPU-Optimizations/Jetson_CPP_Server/Makefile. To note that this is not a Makefile that can be executed with the make command. “cat” the contents of the file and enter it in the command line to execute and generate the required output binary


Section 4: Tools and Dependencies
---------------------------------
The following are the tools and dependencies required to be set up before beginning with the experimentation

1) First check if the GPU is a CUDA enabled GPU. Get the underlying GPU details from the target machine. Using this information, the NVIDIA official website can be visited to check for CUDA compatibility. This experiment will run only on a CUDA enabled GPU. The link from the NVIDIA official website can be found in https://developer.nvidia.com/cuda-gpus

2) The necessary GPU drivers are needed to communicate with the underlying GPU. This can also be done by visiting the NVIDIA official website and comparing the GPU model and downloading the latest and most compatible drivers for the project. The link from the NVIDIA official website can be found https://www.nvidia.com/Download/index.aspx?lang=en-us .

3) Download the latest CUDA Drivers from the NVIDIA official site as well. Kindly make sure if the latest CUDA versions are stable enough. This procedure will bring with itself the nvcc compiler which can compile both CPP and CUDA programs. The CUDA version used for the project is CUDA 9.1. The link from the NVIDIA official website can be found https://developer.nvidia.com/cuda-downloads

4) When the CUDA drivers are downloaded, inside its folder structure is present a folder called samples folder. Run the deviceQuery file present in it, which will give a complete output of all the physical features of the GPU as in the number of cores and the maximum number of parallel threads that can be launched. This is a very useful parameter. A sample screenshot is given in the report (/root/GPU-Optimizations/GPU_Optimization_Report.pdf) for the NVIDIA Jetson Tx2 board. The last line of the image reflects as to where the deviceQuery program is present although it varies in different versions of CUDA

5) The C++ standard used is c++11 and is recommended to use that as it contains all the STL packages and the TCP port handling code

6) The major dependency from the Python part is the paho-mqtt client library. The link for the package can be found https://pypi.org/project/paho-mqtt/

7) Other minor dependencies in the Python part include the packages for json handling, tcp port handling and numpy for graphical output handling
 
8) The IDE used is VSCode. It is optional and can be chosen at will. But it is to be noted that if the code is run in debug mode from any IDE, the timing performance is worse than actually expected. This is because in the debug mode, the core clocks of the CPU and GPU run at lower speeds. Therefore it is always advised to run the code in the "Run" mode or launch the generated binary from a shell. The link for the VSCode download can be found https://code.visualstudio.com/download

9) For profiling at the GPU end, various tools are available as per the model of the GPU and can be referenced from the NVIDIA Website as no one tool is available across all platforms. For example, in the Jetson Tx2 board there is a separate script called as tegrastats present in the home folder that does all the monitoring activity (Power and temperature), whereas in the 1080 chipset, there is a utility called nvidia-smi that does this activity. 
