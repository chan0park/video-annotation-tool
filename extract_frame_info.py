#!/usr/bin/env python
# Extract information of each 1s frame
# e.g., event_occured, mouse_location
import os
import re
import csv
import ast
from image_diff import *
from image_to_text import extract_text

def find_mouse(cnts):
    mouse_cnt = 0
    mouse_locs = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w > 15 and h > 15:
            # print("mouse located on {},{}".format(x,y))
            mouse_cnt += 1
            mouse_locs.append((x,y))
    return mouse_cnt, mouse_locs

def isEvent(score):
    if score<0.9:
        return True
    else:
        return False

def combine_time_script_csv(script_dir='./scripts/', frame_dir='./frames/'):
    time_texts = [x for x in os.listdir(script_dir) if x.endswith('_time.txt')]
    for text_name in time_texts:
        file_name = text_name.replace('_time.txt','')
        if not os.path.isfile(frame_dir+file_name+'.csv'):
            break
        with open(script_dir+text_name, 'r') as file:
            text = file.read()

        with open(frame_dir+file_name+'.csv', 'r') as file:
            reader = csv.reader(file)
            csv_list = list(reader)
        
        text = ast.literal_eval(text)
        for script in text:
            csv_list[int(script[0])+1].append(script[1])

        with open(frame_dir+file_name+'_time.csv', 'w') as file:                                    
            writer = csv.writer(file)                                                       
            writer.writerows(csv_list)
        

def extract_frame_info(image_dir='./images/', frames_dir='./frames'):
    video_folders = [x for x in os.listdir(image_dir) if os.path.isdir(image_dir+x)]
    if not os.path.isdir(frames_dir):
        os.mkdir(frames_dir)

    for video in video_folders:
        print("FRAME_INFO_EXTRACTION: started processing on "+video)
        base_dir = image_dir+video+'/'
        images = os.listdir(base_dir)
        images = [x for x in images if x.endswith('.png')]
        images = sorted(images, key=lambda x: (int(re.sub('\D','',x)),x))
        row_list = []
        row_list.append(['file_name', 'sec','sim', 'contour No', 'mouse No.', 'mouse loc', 'event', 'text', 'script'])
        row_list.append([video, 0, False, False, False, False, False, False, False])

        for i in range(1, len(images)):
            diff, score = diff_and_sim_score(base_dir+images[i], base_dir+images[i-1])
            contours = find_contours(diff)
            mouse_cnt, mouse_locs = find_mouse(contours)
            text = extract_text(base_dir+images[i])
            row_list.append([video, i, score, len(contours), mouse_cnt, mouse_locs, isEvent(score), text])
            
        file = open(frames_dir+video+'.csv','w', newline='\n')
        wr =  csv.writer(file)
        for row in row_list:
            wr.writerow(row)
        file.close()
    combine_time_script_csv(script_dir='./scripts/')

if __name__ == "__main__":
    IMAGE_DIR = './images/'
    FRAMES_DIR = './frames/'
    extract_frame_info(IMAGE_DIR, FRAMES_DIR)

            


