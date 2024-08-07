import argparse
from generate_video import VideoMaker
from generate_questions import GenerateQuestions
import os


def main(n_questions, question_csv_path, output_path, target_element_id,
         template_path, bg_video_folder, bg_audio_folder,
         intro_video=None, question_duration=5, answer_duration=2):

    os.makedirs(output_path, exist_ok=True)
    output_video_file_path = output_path+"/video.mp4"
    output_description_file_path = output_path+"/description.txt"

    bg_videos = list_specific_files(bg_video_folder, {".mp4", ".mov"})
    bg_audio_paths = list_specific_files(bg_audio_folder, {".mp3", ".wav"})

    gq = GenerateQuestions(question_csv_path)
    questions = gq.get_n_questions(n_questions)


    with open(output_description_file_path, 'w+') as f:
        for q in questions:
            f.write(q['question_data']["id_question"]+"\n")


    vm = VideoMaker(template_path, target_element_id, intro_video,
                    bg_videos_paths=bg_videos, bg_audio_paths=bg_audio_paths,
                    question_duration=question_duration, answer_duration=answer_duration
                    )

    vm.make_video(questions, output_video_file_path)


def list_specific_files(directory, extensions={}):
    files = [os.path.join(directory, f) for f in os.listdir(directory) 
             if os.path.isfile(os.path.join(directory, f))
             and os.path.splitext(f)[1].lower() in extensions]
    return files



if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Make a video from questons')
    parser.add_argument('n_questions', type=int, help='Number of questions')
    parser.add_argument('question_csv_path', type=str, help='Path to the questions CSV file')
    parser.add_argument('output_path', type=str, help='Path for the output folder')
    parser.add_argument('--target_element_id', type=str, default="id_slide", help='Target element ID for the video')
    parser.add_argument('--template_path', type=str, default='data/slide_html_templates/slide_template.html', help='Path to the template file')
    parser.add_argument('--bg_video_folder', type=str, default='data/bg' ,help='Path to the background video folder')
    parser.add_argument('--bg_audio_folder', type=str, default='data/bg_audio', help='Path to the background audio folder')
    parser.add_argument('--intro_video', type=str, default=None, help='Path to the intro video')
    parser.add_argument('--question_duration', type=int, default=5, help='Duration for each question')
    parser.add_argument('--answer_duration', type=int, default=2, help='Duration for each answer')

    args = parser.parse_args()

    main(
        args.n_questions,
        args.question_csv_path,
        args.output_path,
        args.target_element_id,
        args.template_path,
        args.bg_video_folder,
        args.bg_audio_folder,
        args.intro_video,
        args.question_duration,
        args.answer_duration
    )
