#!/usr/bin/python
#
# This script broadcasts a live video stream from the camera to a remote render machine.
# the script receiveJPEG.sh or receive264.sh must be running on the remote machine.
# input[0] is the sensor-id allowed values are 0,1,2
# input[1] the ip address of the remote machine
# input[2] is the streaming mode 0 for jpeg, 1 for h.264
#


import sys
import atexit
import subprocess

def printHelp():
    print("grab broadcast video from camera to remote machine")
    print("---------------------------------")
    print("broadcast.py sensor-id remoteMachineIP streamingFormat(0 for jpeg, 1 for h.264")
    print("--help or -h prints help message and exits")

def main():
        inputs=sys.argv[1:]
        if len(inputs)==3:
            sid=inputs[0]
            hostip=inputs[1]
            port=5000
            if inputs[2]==str(0):
                cmd="gst-launch-1.0  nvcamerasrc fpsRange=\"30.0 30.0\" sensor-id="+str(sid)+"' ! 'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,"
                cmd=cmd+"format=(string)I420, framerate=(fraction)30/1'  ! nvjpegenc ! rtpjpegpay ! udpsink host=$hostip port=$port"
                subprocess.call(cmd,shell=True)
            elif inputs[2]==str(1):
                fname=test.h264
                #h264 encode+stream over network
                cmd="gst-launch-1.0 -e nvcamerasrc num-buffers=300  fpsRange=\"30.0 30.0\" sensor-id="+str(sid)
                cmd=cmd+"! 'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)I420, framerate=(fraction)30/1' "
                cmd=cmd+"! nvvidconv flip-method=2 ! 'video/x-raw(memory:NVMM), format=(string)I420' ! tee name=streams streams. ! omxh264enc ! "
                cmd=cmd+"'video/x-h264, stream-format=(string)byte-stream' ! h264parse ! rtph264pay mtu=1400 ! udpsink host=$hostip port=$port streams. "
                cmd=cmd+"! omxh264enc bitrate=8000000 ! 'video/x-h264, stream-format=(string)byte-stream' ! filesink location=$fname"
                subprocess.call(cmd,shell=True)
            else:
                printHelp()
        else:
                printHelp()


if __name__ == '__main__':
        main()
