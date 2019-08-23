import vapoursynth as vs
core = vs.get_core()
import havsfunc as havs

#clip = core.ffms2.Source(video)
clip = core.imwri.Read(video)
#clip = core.msmoosh.MSharpen(clip, threshold=1.0, strength=89)
clip = core.fmtc.matrix (clip, mat="709", col_fam=vs.YUV, bits=16)
clip = core.fmtc.resample (clip, css="420")
clip = core.fmtc.bitdepth (clip, bits=8)
clip = havs.MCTemporalDenoise(clip, settings="very high", MVsharp=2)
clip = core.fmtc.resample (clip, css="444")
clip = core.fmtc.matrix (clip, mat="709", col_fam=vs.RGB)
clip = core.fmtc.bitdepth (clip, bits=8)
clip = core.imwri.Write(clip, "PNG", video, overwrite = True)
clip.set_output()