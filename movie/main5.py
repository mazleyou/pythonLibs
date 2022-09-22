import moviepy.editor as mpe
my_clip = mpe.VideoFileClip('vidout.mp4')
audio_background = mpe.AudioFileClip('eng.wav')
# final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(audio_background)
final_clip.write_videofile("vidout2.mp4", audio=True)