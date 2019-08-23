import vapoursynth as vs
core = vs.get_core()
import os
import havsfunc as havs

video = video.decode("utf-8")
video = video.split(".")[0]
moviefolder = "F:\\JavPlayer v1.03_win64_Nvidia\\Movie\\"
clip1 = moviefolder + video + "_l_000v.mp4"
clip2 = moviefolder + video + "_r_000v.mp4"
clip1 = core.ffms2.Source(clip1)
clip2 = core.ffms2.Source(clip2)
lutdir = "F:\\tocrashplan\\luts\\"
luts = []
mode = 1

#Stupid recursive function for finding LUT .cubes
for file in os.listdir(lutdir):
    #print(lutdir + file)
    if file.lower().endswith(".cube"):
        luts.append(lutdir + file)
    elif os.path.isdir(lutdir + file):
        for thing in os.listdir(lutdir + file):
            if thing.lower().endswith(".cube"):
                luts.append(lutdir + file + "\\" + thing)
                print(lutdir + file + "\\" + thing)
            elif os.path.isdir(lutdir + file + "\\" + thing) == True:
                for sak in os.listdir(lutdir + file + "\\" + thing):
                    if sak.lower().endswith(".cube"):
                        luts.append(lutdir + file + "\\" + thing + "\\" + sak)
                        print(lutdir + file + "\\" + thing + "\\" + sak)
		
orgw = clip1.width
if mode == 0:
	clip1 = core.resize.Bilinear(clip1, orgw, orgw)
	clip2 = core.resize.Bilinear(clip2, orgw, orgw)
	clip1 = core.std.Crop(clip1, left=clip1.width/4, right=clip1.width/4)	
	clip2 = core.std.Crop(clip2, left=clip2.width/4, right=clip2.width/4)
	finalclip = core.std.StackHorizontal((clip2, clip1))
	finalclip = core.resize.Bilinear(finalclip, orgw, orgw/2)
elif mode == 1:
	clip1 = core.resize.Bilinear(clip1, orgw, orgw)
	clip2 = core.resize.Bilinear(clip2, orgw, orgw)
	#clip1 = core.std.Crop(clip1, left=clip1.width/4, right=clip1.width/4)
	#clip2 = core.std.Crop(clip2, left=clip2.width/4, right=clip2.width/4)
	finalclip = core.std.StackHorizontal((clip2, clip1))	

'''
for lut in reallynice:
	finalclip = core.resize.Point(finalclip, format=vs.RGB24, matrix_in_s="709", chromaloc_in_s="top_left")
	finalclip = core.timecube.Cube(finalclip, cube=luts[lut])
	#newclip = core.sub.Subtitle(newclip, lut, style="sans-serif,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1", )
	finalclip = core.resize.Point(finalclip, format=vs.YUV420P8, matrix_s="709", chromaloc_s="top_left")
	#clips.append(newclip)'''
#Do temporal denoise for cleaning up artifacts, enable if you want (this process is very slow)
#finalclip = havs.MCTemporalDenoise(finalclip, settings="very high", MVsharp=2)
finalclip.set_output()