#!/usr/bin/env python
# ffmpeg required
import subprocess
import os

def video_to_images(video_dir, image_dir):
    videos = [video_dir+x for x in os.listdir(video_dir)]
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    for video in videos:
        file_name = video.replace(video_dir,'').split('.')[0]
        if not os.path.isdir(image_dir+file_name):
            os.mkdir(image_dir+file_name)

        cmdline = ['ffmpeg',
                '-y',
                '-i',
                video,
                '-s',
                '2562x1428',
                '-vf',
                'fps=1',
                image_dir+file_name+'/'+file_name+'_%d.png'
                ]
        subprocess.call(cmdline)

if __name__ == "__main__":
    video_to_images('./videos/', './images/')