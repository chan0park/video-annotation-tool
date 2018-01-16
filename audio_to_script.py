#!/usr/bin/env python
import speech_recognition as sr
import os
import re
import time
import argparse
from video_to_audio import split_audio

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=False, default="both",
	help="type of audios you want to process ('sentence' / 'entire' / 'both')")
args = vars(ap.parse_args())

def sentence_audios_to_script(MS_SPEECH_API_KEY, audio_dir='./audios/', script_dir='./scripts/', start_index=0):
    videos = [audio_dir+x for x in os.listdir(audio_dir) if os.path.isdir(audio_dir+x)]
    videos = videos[start_index:]
    if not os.path.isdir(script_dir):
        os.mkdir(script_dir)

    for video in videos:
        sentences = [video+'/'+x for x in os.listdir(video)]
        sentences = sorted(sentences, key=lambda x: (int(re.sub('\D','',x)),x))
        print("start working on "+video)
        script = []
        for i, sentence in enumerate(sentences):
            sec = sentence.replace('.wav','').split('_')[-1]
            if i % 19 == 0:
                print(str(i)+"th file: pausing to avoid getting too many request error")
                time.sleep(65)
            
            r = sr.Recognizer()
            with sr.AudioFile(sentence) as source:
                audio = r.record(source)
            partial_script = r.recognize_bing(audio, key=MS_SPEECH_API_KEY, language = "en-US")
            script.append((sec,partial_script))
            # script = script + " " + partial_script
            # script.append(partial_script)

        with open(script_dir+video.split('/')[-1]+'_time.txt', 'w') as file:
            file.write(str(script))


def entire_videos_to_script(MS_SPEECH_API_KEY, video_dir='./videos/', script_dir='./scripts/'):
    videos = [video_dir+x for x in os.listdir(video_dir) if x.endswith('.mp4')]
    if not os.path.isdir(script_dir):
        os.mkdir(script_dir)

    for video in videos:
        audio_path = './audios/'+video.split('/')[-1].replace('.mp4','.wav')
        split_audio(audio_path, 30, './audios/')
        splited_audios = ['./audios/'+x for x in os.listdir('./audios/') if x.startswith('temp')]
        
        script = ""
        for audio_path in splited_audios:
            r = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = r.record(source)
            partial_script = r.recognize_bing(audio, key=MS_SPEECH_API_KEY, language = "en-US")
            script = script + " " + partial_script
            os.remove(audio_path)
        with open('scripts/'+video.split('/')[-1].replace('.mp4','.txt'), 'w') as file:
            file.write(script)

if __name__ == "__main__":
    MS_SPEECH_API_KEY = "d96401fa16364eb4ab11b685fe7ebd3c"
    if args["mode"] == "both":
        sentence_audios_to_script(MS_SPEECH_API_KEY, start_index=8)
        entire_videos_to_script(MS_SPEECH_API_KEY)
    elif args["mode"] == "sentence":
        sentence_audios_to_script(MS_SPEECH_API_KEY)
    elif args["mode"] == "entire":
        entire_videos_to_script(MS_SPEECH_API_KEY)
    else:
        print("You typed a wrong mode option. Please select from 'both/sentence/entire'")