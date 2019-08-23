import vapoursynth as vs
core = vs.get_core()
import mvsfunc as mvs
core.num_threads = 1
mode = 0
i = int(i.decode("utf-8"))
#ss = int(subsampling.decode("utf-8"))
#actualside = str(side)
clip = core.ffms2.Source(video)
cropl = 0
cropr = 0
cropt = 0
cropb = 0
clips = []
#for i in list(range(16, 32)):
#
width = int(clip.width/i)
height = int(clip.height/i)
if width%2==1:
	ssw = 1
else:
	ssw = 0
if height%2==1:
	ssh = 1
else:
	ssh = 0
#clip2 = clip
#clip = core.msmoosh.MSharpen(clip, threshold=6.0, strength=69)
clip2 = core.resize.Spline36(clip, width=int(clip.width/i)+ssw, height=int(clip.height/i)+ssh)
#clip2 = core.resize.Point(clip2, width=int(clip.width), height=int(clip.width/16)*12)
'''
if int(clip2.width+(clip2.width/6))%2==1:
	ssw = 1
else:
	ssw = 0
if int(clip2.height+(clip2.height/6))%2==1:
	ssh = 1
else:
	ssh = 0
clip2 = core.std.AddBorders(clip2, right=int(clip2.width/6)+ssw, top=int(clip2.height/6)+ssh)
'''
#clip2 = core.resize.Bilinear(clip, width=int(clip.width/i)+ssw, height=200)
#clip2 = core.resize.Bilinear(clip2, width=512, height=256)
#clip2 = clip2[0:30]
#clip2 = core.text.Text(clip2, i)
#clip2 = core.std.Levels(clip2, min_in=0, max_in=255, min_out=10, max_out=255, planes=0)
#clip2 = core.std.Levels(clip2, min_in=0, max_in=255, min_out=3, max_out=255, planes=[1,2])

'''clip2 = core.fmtc.resample (clip=clip2, css="444")
clip2 = core.fmtc.matrix (clip=clip2, mat="709", col_fam=vs.RGB)
clip2 = core.fmtc.bitdepth (clip=clip2, bits=8)
'''
clip2 = mvs.ToRGB(input = clip2, depth = 8)

#clips.append(clip2)
#clip = core.resize.Bilinear(clip, width=clip.width, height=(clip.width/16)*9+ss)
#clips = core.std.Splice(clips)
#clips = core.imwri.Write(clips, "PNG", "F:/blendermosaic/input" + str(i-16) + "/%04d.png", overwrite=True)
clip2.set_output()

