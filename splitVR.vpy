import vapoursynth as vs
core = vs.get_core()

mode = 0
side = side.decode("utf-8") 
ss = int(subsampling.decode("utf-8"))
#actualside = str(side)
clip = core.ffms2.Source(video)
cropl = 0
cropr = 0
cropt = 0
cropb = 0
if side == "l":
	if mode == 0:
		clip = core.std.Crop(clip, left=clip.width/2, right=0)
		#clip = core.resize.Bilinear(clip, width=clip.width, height=(clip.width/16)*9+ss)
		#clip = core.resize.Bilinear(clip, width=clip.width*1.33+ss, height=clip.width)
		#clip = core.resize.Bilinear(clip, width=clip.width*1.77+ss, height=clip.width)
		clip = core.resize.Bilinear(clip, width=clip.width, height=clip.width)
		#orgclip = clip
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=15, max_out=255, planes=0)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=3, max_out=255, planes=[1,2])
		#clip = core.std.Crop(clip, left=clip.width/4+cropl, right=clip.width/4+cropr, top=clip.height/4+cropt, bottom=clip.height/4+cropb)
		#clip = core.resize.Spline36(clip, width=orgclip.width, height=orgclip.height)
	else:
		clip = core.std.Crop(clip, top=clip.height/2, right=0)
		clip = core.std.Crop(clip, left=clip.width/4+cropl, right=clip.width/4+cropr)
		#clip = core.resize.Bilinear(clip, width=clip.width, height=(clip.width/16)*9+ss)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=15, max_out=255, planes=0)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=3, max_out=255, planes=[1,2])
		#clip = core.std.Crop
	#clip = core.sub.Subtitle(clip, side, style="sans-serif,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1", )

elif side == "r":
	if mode == 0:
		clip = core.std.Crop(clip, left=0, right=clip.width/2)
		#clip = core.resize.Bilinear(clip, width=clip.width, height=(clip.width/16)*9+ss)
		#clip = core.resize.Bilinear(clip, width=clip.width*1.33+ss, height=clip.width)
		#clip = core.resize.Bilinear(clip, width=clip.width*1.77+ss, height=clip.width)
		clip = core.resize.Bilinear(clip, width=clip.width, height=clip.width)
		#orgclip = clip
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=15, max_out=255, planes=0)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=3, max_out=255, planes=[1,2])
		#clip = core.std.Crop(clip, left=clip.width/4+cropl, right=clip.width/4+cropr, top=clip.height/4+cropt, bottom=clip.height/4+cropb)
		#clip = core.resize.Spline36(clip, width=orgclip.width, height=orgclip.height)
	else:
		clip = core.std.Crop(clip, top=0, bottom=clip.width/2)
		clip = core.std.Crop(clip, left=clip.width/4+cropl, right=clip.width/4+cropr)
		#clip = core.resize.Bilinear(clip, width=clip.width, height=(clip.width/16)*9+ss)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=15, max_out=255, planes=0)
		clip = core.std.Levels(clip, min_in=0, max_in=255, min_out=3, max_out=255, planes=[1,2])
	#clip = core.sub.Subtitle(clip, side, style="sans-serif,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1", )
clip.set_output()

