# video-annotation-tool

This repository is for a GUI video annotation tool implemented with PyQT5 and Python. With this, you can easily annotate/label  segments of videos and save the segment_list in JSON format for further use.

I also implemented some codes that extract information from each frame image of videos. For each second in video, with its image, you can extract **script text** (what has been said in the video at the moment), whether an **event occured** (by looking at image similarity between the image following on next second), **approixmate mouse cursor location**.

Currently, this tool analyzes the [tutorial videos](https://helpx.adobe.com/creative-cloud/tutorials-explore.html) from Adobe official websites. After the manual annotation process to get sufficient training data, I'm looking forward to do some further research on automatic segmentation (spliting video into segments in contentwise) and tool/behavior classification on each segment. This study is expected to be extended to a wider topic such as automatic video summarization.

## Overview

### Demo Video
<img src="https://media.giphy.com/media/l49JD9VXlMwgcOA5a/giphy.gif" width="680px">
Launch the tool just by typing `python annotation-tool.py`

### Features
- Playlist/ Basic video player features
- Script box
- Segment list/ Segment input box
- New Segment/ Add to the list / Save the list with JSON format

### Output Folders
- Videos/ Audios/ Scripts/ Images/ Frames/ Segments

### Requirements
- Python3
- Homebrew (if you need to install FFmpeg and Tessearact on Mac)
- [FFmpeg](https://www.ffmpeg.org/): `brew install ffmpeg` / `sudo apt-get install ffmpeg`
- [Tesseract](https://github.com/tesseract-ocr/tesseract): `brew install tesseract` / `sudo apt-get install tesseract`
- Python libraries (listed in `requirements.txt`): `pip3 install -r requirements.txt`  
I highly recommend you to use *virtualenv* to install Python libraries!

## video-annotation-tool

### `video_crawling.py`
This code crawls and downloads [Adobe tutorial videos](https://helpx.adobe.com/creative-cloud/tutorials-explore.html).
In total, 25 videos are downloaded from 9 articles in the tutorial website.

### `annotation-tool.py`
`python annotation-tool.py` executes the GUI annotator. 

## Information Extraction codes
### `video_to_audio.py`
FFmpeg required.
Converts video(.mp4) to audio(.wav) for speech recognition. 

### `audio_to_sentences.py`
with given input audio file of one video, it outputs *video_0_0_x.wav* where x denotes starting time of sentences in seconds.
This splits an audio file to a sentence-level, in order to map sentence text to appropriate time. 

*note: it may take some time.*

### `audio_to_script.py`
output: video_0_0_x.txt or video_0_0.txt

This code converts audio to text using the Speech Recognition API from Microsoft Bing. It's excuted as `python audio_to_script.py --mode "both"`. The mode should be specified among ("both"/"sentence"/"entire").

Also, in the code, you should **change the `MS_SPEECH_API_KEY` parameter with your own key**.
To get the API key, go to the [Microsoft Azure Portal Resources](https://portal.azure.com/) page, go to "All Resources" > "Add" > "See All" > Search "Bing Speech API > "Create", and fill in the form to make a "Bing Speech API" resource. On the resulting page (which is also accessible from the "All Resources" page in the Azure Portal), go to the "Show Access Keys" page, which will have two API keys, either of which can be used for the key parameter.

*note: it may take some time, and sometimes failes due to the network connection issue.*

### `video_to_images.py`
output: video_0_0/video_0_0_1.png

Extract one representative image for each second in a video. We extract informations from this image.

### `extract_frame_info.py`
output: frames/video_0_0.csv
dependency: `image_diff.py` / `image_to_text.py`

Extracts information from video images. In `image_diff.py`, calculates the difference between one target image and the previous frame image. If its difference exceeds a certain threshold, we labels the image as 'Event occured'. In `image_to_text.py`, we conduct OCR using Tesseract. Some fundamental pre-processing on images are also included to enhance the OCR performance. 

At the end, we append the script sentence text information. Resulting csv file looks like this.
![Imgur](https://i.imgur.com/uWXWzaY.png)

## Further research direction
The ultimate goal of this annotator, and feature extraction is to enable structured video summarization. To this end, first we need to segment the video in a semantic unit (which holds the same topic), then figure out the content of each segment. This repository will help researchers to collect training data (of segmentation) easily to move on to the next level. With this context being said, I'd like to briefly give my thoughts on future research to achieve the primary goal.

### Automatic Segmentation
As everyone would expect, I also believe that it would not be an easy task because of its subjectivity. I tried to do some annotation on the collected videos, but at some points, it was often ambiguous to say when the new topic has been started. Also, the size/unit of segments may be subjective to annotator, so I believe the researchers should be aware of this issue and handle carefully.

For the actual automatic segmentation, I think the event sequence information could help. I found many cases follow one pattern, (less-relevant-supplement info.)+'explain the objective'+'explain what the instructer will do (action)'+'do action'+'explain what the instructer did'. 

'do action' part is easy to detect (actually, accuracy of my Event column in result csv file was surprisingly high). 'explain what the instructer did' is relatively easy to separate since instructors usually give some *cue words* such as 'next', 'now'. Therefore, if we detect the action properly, it should be easier to find segmentation point.

To me, separating 'less-relevant-supplemental info.' and 'explain the objective' before the action seems like the most challenging part. We should excludes the supplemental information in summary and should mainly use the 'explain the objective' part to connect *explanation* and *action* provided in video tutorials. 

### Entity/Behavior Classification
