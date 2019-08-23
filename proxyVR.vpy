import vapoursynth as vs
core = vs.get_core()

core.num_threads = 8

mode = 0
#i = int(i.decode("utf-8"))
#ss = int(subsampling.decode("utf-8"))
#actualside = str(side)
clip = core.ffms2.Source(video)
width = clip.width/8
height = clip.height/8
clip = core.resize.Bilinear(clip, width=width, height=height)
clip.set_output()

