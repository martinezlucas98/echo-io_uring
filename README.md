# A very basic io_uring echo server (and a regular echo server) benchmark

* __Linux 5.7 or higher with IORING_FEAT_FAST_POLL and IORING_OP_PROVIDE_BUFFERS required__


## Install and run

#### Jens Axboe's liburing is required. This library can be installed by:

`git clone https://github.com/axboe/liburing`

`./configure`

`make`

`make install`


#### Running this project in three steps:

1. First we clone this repo (obviously)

`git clone https://github.com/martinezlucas98/echo-io_uring.git`

> Of course you can do it via ssh if you prefer

2. Install the dependencies

(Optional: use a virtual env)

`cd echo-io_uring`

`pip3 install -r dependencies.txt`

3. Run the python script that builds (or re-builds) the .c binaries and runs the benchmark tool

`python3 benchmark/benchmark.py`

