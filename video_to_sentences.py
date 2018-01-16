#!/usr/bin/env python3
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


def split_on_silence(audio_segment, min_silence_len=1000, silence_thresh=-16, keep_silence=100,
                     seek_step=1):
    """
    audio_segment - original pydub.AudioSegment() object
    min_silence_len - (in ms) minimum length of a silence to be used for
        a split. default: 1000ms
    silence_thresh - (in dBFS) anything quieter than this will be
        considered silence. default: -16dBFS
    keep_silence - (in ms) amount of silence to leave at the beginning
        and end of the chunks. Keeps the sound from sounding like it is
        abruptly cut off. (default: 100ms)
    """

    not_silence_ranges = detect_nonsilent(audio_segment, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    chunks = []
    start_points = []
    for start_i, end_i in not_silence_ranges:
        start_i = max(0, start_i - keep_silence)
        end_i += keep_silence
        start_points.append(start_i)
        chunks.append(audio_segment[start_i:end_i])

    return chunks, start_points

def split_audio_to_sentences(audio_path):
    audio_name = audio_path.split('/')[-1].replace('.wav','')
    sound_file = AudioSegment.from_wav(audio_path)

    print("Processing on "+audio_name)
    # The parameters for min_silence_len and silence_thresh is manually determined by observing the audio files.
    audio_chunks, start_points = split_on_silence(sound_file, min_silence_len=300, silence_thresh=-42)
    

    if not os.path.isdir(audio_path.replace('.wav','')):
        os.mkdir(audio_path.replace('.wav',''))
    for i, chunk in enumerate(audio_chunks):
        out_file = audio_path.replace('.wav','')+'/'+audio_name+"_{0}.wav".format(int(start_points[i]/1000))
        chunk.export(out_file, format="wav")

def audios_to_sentences(AUDIO_DIR = './audios/'):
    audios = [AUDIO_DIR+x for x in os.listdir(AUDIO_DIR) if x.endswith('.wav')]
    for audio in audios:
        split_audio_to_sentences(audio)


if __name__ == "__main__":
    audios_to_sentences('./audios/')