#!/usr/bin/env python
# ffmpeg or avconv required.
# if not, install it with 'brew install ffmpeg' or 'sudo apt-get install ffmpeg'

import subprocess
import os
import time

def video_to_audio(video_path):
    audio_name = video_path.split('/')[-1].replace('.mp4','.wav')
    cmdline = ['ffmpeg',
            '-y',
            '-i',
            video_path,
            'audios/'+audio_name]
    subprocess.call(cmdline)

def videos_to_audio(videos_dir='./videos/', output_audio_dir='./audios/'):
    if not os.path.isdir(output_audio_dir):
        os.mkdir(output_audio_dir)
    videos = os.listdir(videos_dir)
    for video in videos:
        audio_name = video.replace('.mp4','.wav')
        audio_path = output_audio_dir+audio_name
        if not os.path.isfile(audio_path):
            video_to_audio(videos_dir+video)

def split_audio(audio_path, split_time=30, out_dir="./audios/temp/"):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    cmdline = ['ffmpeg',
            '-i',
            audio_path,
            '-f', 'segment' ,'-segment_time', str(split_time), '-c', 'copy', out_dir+'temp%02d.wav']
    subprocess.call(cmdline)

if __name__ == "__main__":
    videos_to_audio()