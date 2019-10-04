#!/bin/bash
#source: https://desertbot.io/blog/how-to-stream-the-picamera
h=`hostname -I`
echo " in the remote browser type:  http://${h}:8080/?action=stream"
cd /home/pi/programs/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"
