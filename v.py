import subprocess
import sys
import os

'''
VR helper scripts
Prerequisites: 
Vapoursynth (fatpack portable version should work) add vspipe to PATH system variable
Python (put this script in PYTHONPATH)
ffmpeg

I recommend splitting the original video into smaller videos for sync purposes.
'''

#Example:
#v.py -s inputfile.mp4
arg = sys.argv[1]

if arg == "-s":
    '''
    Split original video into _l and _r files for further processing
    Usage:
    v.py -s inputfile.mp4
    If you get an error because of subsampling (resizing) do:
    v.py -s inputfile.mp4 1
    '''
    sides = ["l", "r"]
    file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0
    finalpath = os.getcwd() + "\\" + file
    bitrate = 25
    #Set encoding settings here (I use h264_nvenc for speed)
    encodingstring =  "-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high", 

    for i, side in enumerate(sides):
        command = ["vspipe", "-a", "video=" + finalpath, "-a", "side=" + side, "-a", "subsampling=" + str(subsampling), "--y4m", "C://VSEdit//splitVR.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p", encodingstring, "-y", file.split(".")[0] + "_" + side + ".mp4"]
        subprocess.call(command, shell = True)

elif arg == "-c":
    '''
    Combine processed _l and _r videos into one video. Input is the file you used with v.py -s so you can just switch the letter
    Usage:
    v.py -c inputfile.mp4
    '''
    file = sys.argv[2]
    finalpath = os.getcwd() + "\\" + file
    #This bitrate is for discord, for offline use raise it
    bitrate = 12
    #Set encoding settings here (I use h264_nvenc for speed)
    encodingstring =  "-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high",
    command = ["vspipe", "-a", "video=" + file, "--y4m", "C://VSEdit//combinevr.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p", encodingstring, "-y", file.split(".")[0] + "_" + "combined" + ".mp4"]
    command2 = ["ffmpeg.exe", "-i", file.split(".")[0] + "_" + "combined.mp4", "-i",  file, "-map", "0:v", "-map", "1:a", "-shortest", "-c", "copy", "-y", file.split(".")[0] + "_" + "final" + ".mp4"]
    subprocess.call(command, shell = True)
    subprocess.call(command2, shell = True)
    os.remove(file.split(".")[0] + "_" + "combined.mp4")

elif arg == "-l":
    '''
    Create video of preview LUTs for color grading (note: not used yet in main script)
    '''
    file = sys.argv[2]
    finalpath = os.getcwd() + "\\" + file
    bitrate = 4
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    command = ["vspipe", "-a", "video=" + finalpath, "-a", "subsampling=" + str(subsampling), "--y4m", "C://VSEdit//LUT.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p",  "-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high", "-y", file.split(".")[0] + "_" + "LUT" + ".mp4"]
    subprocess.call(command, shell = True)