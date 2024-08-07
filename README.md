# YTgen

this a simple project for creating video in bulk using a template and populating that template from csv data.
this repo is a proof of concept for the task described above.

## Getting started

place bg_audio (for audio), bg (for video), csv folders in data folder. and fill them with sutable .mp3, .mp4, and .csv files.
videos and audios will be used as background. slides will be overlayed on these videos.
videos should be 1280x720(for now). length of video does not matter.(for now 10s clips are extracted and used randomly)


csv file must have these columns
```txt/csv
question,option_1,option_2,option_3,option_4,correct_option
```
if all the data is placed in the correct folders you can continue with
```shell
python3 -m venv .env
pip install -r requirements.txt
python main.py 2 'data/csv/politics.csv' 'data/output/test01'
```
chrome will open and slides will be snaped. and at the end a video and used questions will be placed in output folder.


other available arguments are below. and can be used insted of creating above folders
```
--target_element_id
--template_path
--bg_video_folder
--bg_audio_folder
--intro_video
--question_duration
--answer_duration
```
detaisl of tese variables are availabel in main file.
