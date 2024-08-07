from slide_parser import SlideParser
from slide_snaper import SlideSnapper
import moviepy.editor as mp
import numpy as np
import random

class VideoMaker:
    def __init__(self, template_path, targert_element_id,
                  intro_video=None, bg_videos_paths=[], bg_audio_paths=[], 
                  question_duration=8, answer_duration=2,
                  slide_size=(920, 460), video_size=(1080, 720)
                  ) -> None:
        self.template_path = template_path 
        self.targert_element_id = targert_element_id 
        self.initial_clip_path = intro_video
        self.bg_paths = bg_videos_paths
        self.bg_audio_paths = bg_audio_paths
        self.question_duration = question_duration
        self.answer_duration = answer_duration
        self.slide_size = slide_size
        self.video_size = video_size


        self.parser = SlideParser(self.template_path)
        self.snapper = SlideSnapper(self.targert_element_id)

        countdown = self.make_countdown(countdown_start=question_duration)
        self.countdown_clip = mp.vfx.mask_color(countdown, color=[0,0,0])



    def make_video(self, questions, output_file):

        full_video = None
        if self.initial_clip_path:
            full_video = mp.VideoFileClip(self.initial_clip_path).resize(newsize=self.slide_size)

        for i, question in enumerate(questions):

            question_data = question['question_data']
            correct_option = question['correct_option']

            # snap without correct option
            parsed_html = self.parser.parse_template(question_data)
            question_image = self.snapper.take_snap_png(page_html=parsed_html)
            # snap with correct option
            parsed_html = self.parser.parse_template(question_data, correct_option)
            marked_image = self.snapper.take_snap_png(page_html=parsed_html)


            question_clip = mp.ImageClip(np.array(question_image)).set_duration(self.question_duration)
            answer_clip = mp.ImageClip(np.array(marked_image)).set_duration(self.answer_duration)

            question_no_clip = mp.TextClip(f"Question {i+1}", fontsize=50,
                                            color='green', bg_color="white",
                                            size=question_clip.size
                                            ).set_duration(0.5)
            countdown_overlay_clip = self.countdown_clip.set_position(
                (question_clip.size[0] - self.countdown_clip.size[0] - 30,
                 question_clip.size[1] - self.countdown_clip.size[1] - 30))

            complete_question = mp.concatenate_videoclips([question_clip, answer_clip])
            complete_question = mp.CompositeVideoClip([complete_question, countdown_overlay_clip])
            # complete_question = mp.concatenate_videoclips([question_no_clip, complete_question])

            if full_video:
                full_video = mp.concatenate_videoclips([full_video, complete_question], transition=question_no_clip)
            else:
                full_video = complete_question
        
        full_video = full_video.set_position("center")

        bg_video = self.make_backgrounds(full_video.duration)

        final_video = mp.CompositeVideoClip([bg_video, full_video])
        final_audio = self.make_audio_clip(final_video.duration)
        final_video = final_video.set_audio(final_audio)

        final_video.write_videofile(output_file, 30)


    def make_backgrounds(self, video_clip_duration, chunk_max_duration=10, bg_size=(1280,720)):

        bg_clip_full = None 
        while bg_clip_full is None or video_clip_duration > bg_clip_full.duration: 
            
            random_bg_path = random.choice(self.bg_paths)

            bg_clip = mp.VideoFileClip(random_bg_path)

            if bg_clip.duration > chunk_max_duration:
                bg_clip = bg_clip.set_duration(chunk_max_duration)
            
            bg_clip = bg_clip.resize(bg_size)

            if bg_clip_full:
                bg_clip_full = mp.concatenate_videoclips([bg_clip_full, bg_clip])
            else:
                bg_clip_full = bg_clip


        return bg_clip_full.set_duration(video_clip_duration)

            
    def make_countdown(self, countdown_start, duration=None, font_size=80, size=(150,110), fps=30):
                
        if duration is None:
            duration = countdown_start

        def make_frame(t):
            remaining_time = int(countdown_start - t)
            text_clip = mp.TextClip(str(remaining_time + 1),
                                    fontsize=font_size,
                                    color='white',
                                    size=(200, 200))
            text_clip = text_clip.set_duration(duration)
            return text_clip.get_frame(t)

        countdown_clip = mp.VideoClip(make_frame, duration=duration)

        countdown_clip = countdown_clip.set_duration(duration).set_fps(fps)
        return countdown_clip
    

    def make_audio_clip(self, required_length):

        audio_file = random.choice(self.bg_audio_paths)
        print("audifile = ", audio_file)
        audio_clip = mp.AudioFileClip(audio_file)
        clip_duration = audio_clip.duration

        if clip_duration >= required_length:
            audio_clip = audio_clip.subclip(0, required_length)
        else:
            num_repeats = int(required_length // clip_duration) + 1
            clips = [audio_clip] * num_repeats
            audio_clip = mp.concatenate_audioclips(clips).subclip(0, required_length)

        return audio_clip
