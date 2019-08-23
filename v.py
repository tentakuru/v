import subprocess
import sys
import os
from natsort import natsorted

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
    encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]

    for i, side in enumerate(sides):
        command = ["vspipe", "-a", "video=" + finalpath, "-a", "side=" + side, "-a", "subsampling=" + str(subsampling), "--y4m", "C://VSEdit//splitVR.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p", *encodingstring, "-y", file.split(".")[0] + "_" + side + ".mp4"]
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
    bitrate = 8
    #Set encoding settings here (I use h264_nvenc for speed)
    encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    command = ["vspipe", "-a", "video=" + file, "--y4m", "C://VSEdit//combinevr.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p", *encodingstring, "-y", file.split(".")[0] + "_" + "combined" + ".mp4"]
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

elif arg == "-b0":
    '''
    Blender part 0 (scale for Blender masking)
    '''
    file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    #for i in list(range(16, 32)):

     #   print(str(int(width)) + " x " + str(int(height)))
    
    finalpath = os.getcwd() + "\\" + file
    bitrate = 5
    #Set encoding settings here (I use h264_nvenc for speed)
    encodingstring =  ["-c:v", "h264_nvenc", "-preset", "fast", "-b:v", str(bitrate) + "M"]
    #encodingstring =  ["-c:v", "libx264", "-b:v", str(bitrate) + "M"]
    #encodingstring = 
    
    ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
    ffprobecommand = ffprobecommand.split(" ")
    ffprobevar = subprocess.check_output(ffprobecommand)
    width, height = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
    width = int(width/4)
    height = int(height/4)
    if width %2 == 1:
        width += 1
    if height %2 == 1:
        height += 1
    
    i = 4
    '''
    try:
        os.makedirs(os.getcwd() + "\\" + file.split(".")[0])
    except:
        pass
    ''' #"
    #"-resize", "1024x512",
    #command = ["C:\\ffmpeg-new\\bin\\ffmpeg.exe", "-vsync", "0", "-hwaccel", "nvdec", "-hwaccel_output_format", "cuda", "-i", file, "-c:a", "copy", "-vf", "scale_npp=1024:512",  *encodingstring, "-y", file.split(".")[0] + "_" + "proxy" + ".mp4"]
    #^#command = ["C:\\ffmpeg-new\\bin\\ffmpeg.exe", "-c:v", "h264_cuvid", "-resize", "1024x512", "-i", file, "-c:a", "copy", *encodingstring, "-y", file.split(".")[0] + "_" + "proxy" + ".mp4"]
    command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-vsync" ,"0", "-hwaccel", "cuvid", "-c:v", "h264_cuvid", "-i", file, "-vf" ,"scale_npp=" + str(width) + ":" + str(height), "-c:a", "copy", *encodingstring, "-y", file.split(".")[0] + "_" + "proxy" + ".mp4",
    "-c:v", "h264_cuvid", "-i", file, "-vf" ,"scale_npp=" + str(width/2) + ":" + str(height/2), "-c:a", "copy", *encodingstring, "-y", file.split(".")[0] + "_" + "proxy2" + ".mp4"]
    
    
    #ffmpeg -vsync 0 –hwaccel cuvid -c:v h264_cuvid -i input.mp4 -c:a copy –vf scale_npp=1280:720:interp_algo=super -c:v h264_nvenc -b:v 5M output_720.mp4
    #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "--y4m", "C://VSEdit//proxyVR.vpy", "-", "|", "C:\\ffmpeg-new\\bin\\ffmpeg.exe", "-vsync", "0", "-hwaccel", "nvdec", "-hwaccel_output_format", "cuda",  "-i", "pipe:", *encodingstring, "-y", file.split(".")[0] + "_" + "proxy" + ".mp4"]

    #command = ["ffmpeg.exe", "-i", file, "-vf", "scale=" + str(width) + ":" + str(height), "-y", os.getcwd() + "\\" + file.split(".")[0] + "\\" + file.split(".")[0] + "_proxy_%04d" + ".jpg"]
#"-hwaccel", "nvdec",
    #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "--y4m", "C://VSEdit//proxyVR.vpy", "-", "|", "ffmpeg.exe",  "-i", "pipe:", *encodingstring, "-y", file.split(".")[0] + "_" + "proxy" + ".mp4"]
    #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
    subprocess.call(command, shell = True)

elif arg == "-image":
    '''
    Blender part 1
    '''
    esrgan = True
    file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    #for i in list(range(16, 32)):

     #   print(str(int(width)) + " x " + str(int(height)))
    
    finalpath = os.getcwd() + "\\" + file
    bitrate = 25
    #Set encoding settings here (I use h264_nvenc for speed)
    #encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    #encodingstring = 
    min = 6
    max = 24
    ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
    ffprobecommand = ffprobecommand.split(" ")
    ffprobevar = subprocess.check_output(ffprobecommand)
    originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
    #originalwidth = originalwidth
    #originalheight = originalwidth / 16 * 12
    for i in list(range(min, max)):
        width = int(originalwidth/i)
        height = int(originalheight/i)
        if width %2 == 1:
            width += 1
        if height %2 == 1:
            height += 1
        if esrgan:
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVResrgan.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05,setsar=1:1", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVResrgan.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05,setsar=1:1", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\image" + "\\" + str(i) + "_%04d" + ".png"]
        else:
            command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05,setsar=1:1", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
        subprocess.call(command, shell = True)


elif arg == "-b1":
    '''
    Blender part 1
    '''
    esrgan = False
    file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    #for i in list(range(16, 32)):

     #   print(str(int(width)) + " x " + str(int(height)))
    
    finalpath = os.getcwd() + "\\" + file
    bitrate = 25
    #Set encoding settings here (I use h264_nvenc for speed)
    #encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    #encodingstring = 
    min = 4
    max = 16
    ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
    ffprobecommand = ffprobecommand.split(" ")
    ffprobevar = subprocess.check_output(ffprobecommand)
    originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
    #originalwidth = originalwidth
    #originalheight = originalwidth / 16 * 12
    for i in list(range(min, max)):
        try:
            os.makedirs(os.getcwd() + "\\input" + str(i-min))
        except:
            pass

        width = int(originalwidth/i)
        height = int(originalheight/i)
        if width %2 == 1:
            width += 1
        if height %2 == 1:
            height += 1
        if esrgan:
            command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVResrgan.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05,setsar=1:1", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
        else:
            command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05,setsar=1:1", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
        subprocess.call(command, shell = True)

elif arg == "-b1alt":
    '''
    Blender part 1
    '''
    file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    #for i in list(range(16, 32)):

     #   print(str(int(width)) + " x " + str(int(height)))
    
    finalpath = os.getcwd() + "\\" + file
    bitrate = 25
    #Set encoding settings here (I use h264_nvenc for speed)
    #encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    #encodingstring = 
    min = 20
    max = 40  
    ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
    ffprobecommand = ffprobecommand.split(" ")
    ffprobevar = subprocess.check_output(ffprobecommand)
    originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]

    commands = []
    
    #command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-vsync" ,"0", "-hwaccel", "nvdec", "-hwaccel_output_format", "cuda"]
    
    #command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-vsync" ,"0", "-hwaccel", "cuvid"]

    for i in list(range(min, max)):
        try:
            os.makedirs(os.getcwd() + "\\input" + str(i-min))
        except:
            pass
        width = int(originalwidth/i)
        height = int(originalheight/i)
        if width %2 == 1:
            width += 1
        if height %2 == 1:
            height += 1
        #"-discard", "nokey",
        #    #"-c:v", "h264_cuvid", "-i", file, "-vf" ,"scale_npp=" + str(width/2) + ":" + str(height/2), "-c:a", "copy", "-y", file.split(".")[0] + "_" + "proxy2" + ".mp4"]
    # "-y", os.getcwd() + "\\input" + str(i-16) + "\\%04d" + ".png"
    
        #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-r", "59.94", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-16) + "\\%04d" + ".png"]
        #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
        
        #command = ["vspipe", "-a", "video=" + finalpath, "C://VSEdit//convertRGB.vpy", "-", "|"]
        command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-vsync" ,"0", "-hwaccel", "cuvid"]
        command.extend(["-c:v", "h264_cuvid", "-resize", str(width) + "x" + str(height), "-i", file, "-vf" ,"hwdownload,format=nv12,colorlevels=romin=0.05:gomin=0.05:bomin=0.05",  "-pix_fmt", "rgb24", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
        #command.extend(["-c:v", "h264_cuvid", "-i", file, "-vf" ,"scale_npp=" + str(width) + ":" + str(height) + ":interp_algo=super,hwdownload,format=nv12,colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-pix_fmt", "rgb24", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
        
        subprocess.call(command, shell = True)
        
        '''
        command.extend(["-c:v", "h264_cuvid", "-i", file, "-vf" ,"thumbnail_cuda=2,hwdownload,format=nv12,scale_npp=" + str(width) + ":" + str(height),  "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
    subprocess.call(command, shell = True)
    '''

elif arg == "-b2":
    '''
    Blender part 1
    '''
    tgpath = "C:/tentakuruplayer/TG/"
    f = open(tgpath + "concat.txt", "w+")
    for folder in natsorted(os.listdir(tgpath)):
        if folder.startswith("output"):
                    
            #file = sys.argv[2]

            #for i in list(range(16, 32)):

            #   print(str(int(width)) + " x " + str(int(height)))
            
            #finalpath = os.getcwd() + "\\" + file
            bitrate = 10
            #Set encoding settings here (I use h264_nvenc for speed)
            encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
            #encodingstring = 
            '''
            min = 14
            max = 30
            ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
            ffprobecommand = ffprobecommand.split(" ")
            ffprobevar = subprocess.check_output(ffprobecommand)
            originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
            width = int(originalwidth/i)
            height = int(originalheight/i)
            if width %2 == 1:
                width += 1
            if height %2 == 1:
                height += 1
            '''
            width = 640
            height = 480
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
            command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-hwaccel", "nvdec"]
            #command.extend(["-c:v", "h264_cuvid", "-resize", str(width) + "x" + str(height), "-i", file, "-vf" ,"hwdownload,format=nv12,colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
            command.extend(["-i", tgpath + "\\" + folder + "\\" + "output_%04d.jpg", "-vf" ,"scale=" + str(width) + ":" + str(height), "-y", "-r", "29.97", *encodingstring, tgpath + "\\" + folder + "\\" + folder + ".mp4"])        
            subprocess.call(command, shell = True)
            f.write("file " + tgpath + folder + "/" + folder + ".mp4 \n")
        
    concat = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-y", *encodingstring, tgpath + "combined_output.mp4"]
    f.close()        
    subprocess.call(concat, shell=True)

elif arg == "-b2alt":
    '''
    Blender part 1
    '''
    tgpath = "C:/tentakuruplayer/TG/"
    f = open(tgpath + "concat.txt", "w+")
    for folder in natsorted(os.listdir(tgpath)):
        if folder.startswith("output"):
                    
            #file = sys.argv[2]

            #for i in list(range(16, 32)):

            #   print(str(int(width)) + " x " + str(int(height)))
            
            #finalpath = os.getcwd() + "\\" + file
            bitrate = 10
            #Set encoding settings here (I use h264_nvenc for speed)
            encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
            #encodingstring = 
            '''
            min = 14
            max = 30
            ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
            ffprobecommand = ffprobecommand.split(" ")
            ffprobevar = subprocess.check_output(ffprobecommand)
            originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
            width = int(originalwidth/i)
            height = int(originalheight/i)
            if width %2 == 1:
                width += 1
            if height %2 == 1:
                height += 1
            '''
            width = 640
            height = 480
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
            command = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-hwaccel", "nvdec"]
            #command.extend(["-c:v", "h264_cuvid", "-resize", str(width) + "x" + str(height), "-i", file, "-vf" ,"hwdownload,format=nv12,colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
            command.extend(["-i", tgpath + "\\" + folder + "\\" + "output_%04d.png", "-vf" ,"scale=" + str(width) + ":" + str(height), "-y", "-r", "29.97", *encodingstring, tgpath + "\\" + folder + "\\" + folder + ".mp4"])        
            subprocess.call(command, shell = True)
            f.write("file " + tgpath + folder + "/" + folder + ".mp4 \n")
        
    concat = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-y", *encodingstring, tgpath + "combined_output.mp4"]
    f.close()        
    subprocess.call(concat, shell=True)




elif arg == "-b3":
    '''
    Blender part 2
    '''
    #file = sys.argv[2]
    try:
        subsampling = sys.argv[3]
    except:
        subsampling = 0

    #for i in list(range(16, 32)):

     #   print(str(int(width)) + " x " + str(int(height)))
    
    #finalpath = os.getcwd() + "\\" + file
    bitrate = 25
    #Set encoding settings here (I use h264_nvenc for speed)
    #encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    #encodingstring = 
    encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    
    for folder in os.listdir("C:\\tentakuruplayer\\TG\\"):
        if folder.startswith("output"):
            command = ["ffmpeg.exe", "-r", "59.94", "-i", "C:\\tentakuruplayer\\TG\\" + folder + "\\" + "output_%04d.jpg", "-pix_fmt", "yuv420p", *encodingstring, "-y", "C:\\tentakuruplayer\\TG\\" + folder + "\\" + "output" + ".mp4"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-r", "59.94", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-16) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
            subprocess.call(command, shell = True)


elif arg == "-b4":
    '''
    Blender part 3
    '''
    file = sys.argv[2]
    mask = os.getcwd() + "\\" + "mask.mp4"
    i = 0
    teco = "C:\\tentakuruplayer\\TG\\output" + str(i) + "\\output.mp4"
    finalpath = os.getcwd() + "\\" + file
    #This bitrate is for discord, for offline use raise it
    bitrate = 7
    #Set encoding settings here (I use h264_nvenc for speed)
    encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
    command = ["vspipe", "-a", "video=" + finalpath, "-a", "mask=" + mask, "-a", "teco=" + teco, "--y4m", "C://VSEdit//maskVR.vpy", "-", "|", "ffmpeg.exe", "-i", "pipe:", "-pix_fmt", "yuv420p", *encodingstring, "-y", file.split(".")[0] + "_" + "masked" + ".mp4"]
    command2 = ["ffmpeg.exe", "-i", file.split(".")[0] + "_" + "masked.mp4", "-i",  file, "-map", "0:v", "-map", "1:a", "-shortest", "-c", "copy", "-y", file.split(".")[0] + "_" + "final_output" + ".mp4"]
    subprocess.call(command, shell = True)
    subprocess.call(command2, shell = True)
    os.remove(file.split(".")[0] + "_" + "masked.mp4")

elif arg == "-tweakoutput":
    '''
    Blender part 1
    '''
    tgpath = "F:/JavPlayer v1.03_win64_Nvidia/TG/"
    #f = open(tgpath + "concat.txt", "w+")
    for folder in natsorted(os.listdir(tgpath)):
        if folder.startswith("output"):
                    
            #file = sys.argv[2]

            #for i in list(range(16, 32)):

            #   print(str(int(width)) + " x " + str(int(height)))
            
            finalpath = os.getcwd() + "\\" + folder + "\\" + "output_%04d.png"
            #bitrate = 10
            #Set encoding settings here (I use h264_nvenc for speed)
            #encodingstring =  ["-c:v", "h264_nvenc", "-preset", "medium", "-b:v", str(bitrate) + "M", "-bufsize", str(bitrate*2) + "M", "-profile:v", "high"]
            #encodingstring = 
            '''
            min = 14
            max = 30
            ffprobecommand = "ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x " + file
            ffprobecommand = ffprobecommand.split(" ")
            ffprobevar = subprocess.check_output(ffprobecommand)
            originalwidth, originalheight = [int(i) for i in ffprobevar.decode("utf-8").strip().split("x")]
            width = int(originalwidth/i)
            height = int(originalheight/i)
            if width %2 == 1:
                width += 1
            if height %2 == 1:
                height += 1
            '''
            #width = 640
            #height = 480
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "-", "|", "ffmpeg.exe", "-f", "rawvideo", "-s", str(width) + "x" + str(height), "-pix_fmt", "gbrp", "-i", "-", "-vf", "colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"]
            #command = ["vspipe", "-a", "video=" + finalpath, "-a", "i=" + str(i), "C://VSEdit//resizeVR.vpy", "NUL"]
            command = ["vspipe", "-a", "video=" + finalpath, "C://VSEdit//tweak.vpy", "NUL"]
            #command.extend(["-c:v", "h264_cuvid", "-resize", str(width) + "x" + str(height), "-i", file, "-vf" ,"hwdownload,format=nv12,colorlevels=romin=0.05:gomin=0.05:bomin=0.05", "-f", "image2", "-vcodec", "png", "-y", os.getcwd() + "\\input" + str(i-min) + "\\%04d" + ".png"])        
            #command.extend(["-i", tgpath + "\\" + folder + "\\" + "output_%04d.jpg", "-vf" ,"scale=" + str(width) + ":" + str(height), "-y", "-r", "29.97", *encodingstring, tgpath + "\\" + folder + "\\" + folder + ".mp4"])        
            subprocess.call(command, shell = True)
            #f.write("file " + tgpath + folder + "/" + folder + ".mp4 \n")
        
    #concat = ["C:\\media-autobuild_suite-master\\local64\\bin-video\\ffmpeg.exe", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-y", *encodingstring, tgpath + "combined_output.mp4"]
    #f.close()        
    #subprocess.call(concat, shell=True)
