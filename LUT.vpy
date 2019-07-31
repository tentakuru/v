import vapoursynth as vs
core = vs.get_core()
import muvsfunc as mvf
import adjust
import os
import hysteria as hys
import havsfunc as has

file = video
#file = r'F:\4d\javplayerit\tmafel2_r_000v.mp4'
ss = int(subsampling.decode("utf-8"))
clip = core.ffms2.Source(file)
clip = clip[0]
clip = core.resize.Bilinear(clip, width=clip.width/3+ss, height=clip.height/3)
#clip = clip[177005] + clip[40000] + clip [60000] + clip[80000]
#clip = core.ffms2.Source(
#r'F:\jdownloader\birthday cake_ TWERK _ トゥワークみくり_\birthday cake_ TWERK _ トゥワークみくり_ (2160p_60fps_VP9-128kbit_AAC).mkv')
#clip = mvf.SmoothGrad(clip, radius=150, thr = 5)
#clip = adjust.Tweak(clip, sat=0)
#clip = core.bifrost.Bifrost(clip, variation = 1, luma_thresh = 50, interlaced = True)
#maskclip = core.tcm.TColorMask(clip, ['$C8AE8B'], tolerance=40, bt601=False, gray=True, lutthr=9)
#maskclip = core.std.Levels(maskclip, gamma=1, min_in=0, max_in=220, min_out=0, max_out=255)
#adjustedclip = adjust.Tweak(clip, sat=0, bright=10)
#clip = core.std.MaskedMerge(clip, adjustedclip, maskclip)
#clip = core.flux.SmoothT(clip, temporal_threshold=50)
#clip = core.tmedian.TemporalMedian(clip, radius=1, planes=[0])
#208, 182, 149
#clip = core.resize.Bicubic(clip=clip, format=vs.RGB24)
#clip = core.adjust.Tweak()
#clip2 = core.timecube.Cube(clip, cube="F:\\tocrashplan\\shigoto\\luts\\Ronski-Got-cld.cube")
#niceluts = [1, 9, 12, 18, 22, 25, 26, 29, 35, 40, 44, 46, 48, 49, 50, 53, 55, 58, 67, 68, 69, 71, 76]

crop_string  = ""
#resize_string = "core.resize.Bicubic(input,1280,720,filter_param_a=0,filter_param_b=0.75)"
resize_string = ""
super_params     = "{pel:1,scale:{up:0},gpu:1,full:true,rc:true}"
analyse_params   = "{main:{search:{coarse:{distance:-8},distance:0}}}"
smoothfps_params = "{gpuid:11,rate:{num:72,den:1, abs:true},algo:21,mask:{area:50},scene:{blend:true}}"
def interpolate(clip):
    input = clip
    if crop_string!='':
        input = eval(crop_string)
    if resize_string!='':
        input = eval(resize_string)

    super   = core.svp1.Super(input,super_params)
    vectors = core.svp1.Analyse(super["clip"],super["data"],input,analyse_params)
    smooth  = core.svp2.SmoothFps(input,super["clip"],super["data"],vectors["clip"],vectors["data"],smoothfps_params,src=clip)
    
    smooth  = core.std.AssumeFPS(smooth,fpsnum=smooth.fps_num,fpsden=smooth.fps_den)
    return smooth



niceluts = [2, 7, 22, 40, 46, 49, 68, 69, 70, 79]
luts = []
lutdir = "F:\\tocrashplan\\shigoto\\luts\\"
for file in os.listdir("F:\\tocrashplan\\shigoto\\luts\\"):
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
		
clips = []
#reallynice = [49, 70]
reallynice = [49]
newclip = core.sub.Subtitle(clip, "original colors", style="sans-serif,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1", )
clips.append(newclip*20)

#2, 5, 11, 13, 19, 20, 21
for i, lut in enumerate(luts):
	newclip = core.resize.Point(clip, format=vs.RGB24, matrix_in_s="709", chromaloc_in_s="top_left")
	newclip = core.timecube.Cube(newclip, cube=lut)
	newclip = core.sub.Subtitle(newclip, str(i) + ":" + lut.split("\\")[-1], style="sans-serif,30,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1", )
	newclip = core.resize.Point(newclip, format=vs.YUV420P8, matrix_s="709", chromaloc_s="top_left")
	clips.append(newclip*20)

'''
lutnum = 4
clip = core.resize.Point(clip, format=vs.RGB24, matrix_in_s="709", chromaloc_in_s="top_left")
clip = core.timecube.Cube(clip, cube=luts[niceluts[lutnum]])
clip = core.text.Text(clip, luts[niceluts[lutnum]])'''
#clip = core.timecube.Cube(clip, cube=luts[0])
#clip = core.resize.Point(clip, format=vs.YUV420P8, matrix_s="709", chromaloc_s="top_left")
#clip4 = core.timecube.Cube(clip, cube="F:\\tocrashplan\\shigoto\\luts\\Ronski-Got-mid.cube")
#clip = core.std.Splice(clips)

#clip2 = core.fft3dfilter.FFT3DFilter(newclip, sigma=3, sharpen=2, dehalo=2)
#clip = core.std.Interleave((newclip, clip2))

'''
if stereo_type == 1:
lf = interpolate(core.std.CropRel(clip,0,(int)(clip.width/2),0,0))
rf = interpolate(core.std.CropRel(clip,(int)(clip.width/2),0,0,0))
smooth = core.std.StackHorizontal([lf, rf])
'''
#newclip = core.fft3dfilter.FFT3DFilter(newclip, sigma=2, sharpen=0.8, dehalo=0)
#newclip2 = core.knlm.KNLMeansCL(newclip, d=3, a = 1, s=1, h=3)
#newclip = hys.Hysteria(newclip, strength= 10.0, usemask=True, lowthresh=6, highthresh=20, luma_cap=191, maxchg=255, minchg=0, planes = [0], luma=True, showmask=False)
#
#newclip = core.std.Interleave((newclip, newclip2))
#newclip = has.Deblock_QED(newclip)
#newclip = core.flux.SmoothT(newclip, temporal_threshold=7)
#newclip = core.tmedian.TemporalMedian(clip, radius=1, planes=[0])
#lf = interpolate(core.std.CropRel(newclip,0,(int)(newclip.width/2),0,0))
#rf = interpolate(core.std.CropRel(newclip,(int)(newclip.width/2),0,0,0))
#smooth = core.std.StackHorizontal([lf, rf])
#clip = core.std.Interleave(clips)
clip = core.std.Splice(clips)
clip.set_output()