import vapoursynth as vs
core = vs.get_core()
import mvsfunc as mvs

core.num_threads = 8
mode = 0
#i = int(i.decode("utf-8"))

clip = core.ffms2.Source(video)
teco = core.ffms2.Source(teco) 
'''
teco = core.imwri.Read(teco)
teco = core.fmtc.matrix (teco, mat="709", col_fam=vs.YUV, bits=16)
teco = core.fmtc.resample (teco, css="420")
teco = core.fmtc.bitdepth (teco, bits=8)
'''
mask = core.ffms2.Source(mask)
#for i in list(range(16, 32)):
teco = core.resize.Bicubic(teco, width=clip.width, height=clip.height)
mask = core.resize.Bicubic(mask, width=clip.width, height=clip.height)
clip = core.std.MaskedMerge(clip, teco, mask)

clip.set_output()

