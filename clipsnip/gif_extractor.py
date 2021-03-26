import os
import re
import subprocess

import syllables
from pysubs2 import SSAEvent, SSAFile
from scenedetect.detectors import ContentDetector
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.scene_manager import SceneManager
from scenedetect.video_manager import VideoManager

from clipsnip.config import tmp_dir


class GifExtractor:

    def __init__(self, padding_seconds=1.5):
        self.padding_milliseconds = padding_seconds*1000
        self.output_format = '.mp4'

    def extract_gif(self, source, subtitles_list):

        for subtitles_obj in subtitles_list:

            # gets an estimated start/end time from padding subtitles times
            [start_time_padded, end_time_padded] = self.get_padded_trim_times(subtitles_obj)

            subtitles = subtitles_obj.subs

            # gets frame accurate start/end times for scene cuts
            [trim_start, trim_end] = find_trim_times(source, subtitles, start_time_padded/1000, end_time_padded/1000)

            subtitles.shift(s=-trim_start.get_seconds())
            subtitles = add_effects(subtitles)
            ass_filename = os.path.join(tmp_dir, os.urandom(24).hex() + '.ass')
            subtitles.save(ass_filename)

            output_filename = get_output_name(source, subtitles, self.output_format)
            trim(source, ass_filename, output_filename, trim_start, trim_end)
            os.remove(ass_filename)

    def get_padded_trim_times(self, subtitles):

        start_time_padded = subtitles.subs[0].start - self.padding_milliseconds
        if subtitles.previous_end_time and start_time_padded < subtitles.previous_end_time:
            start_time_padded = subtitles.previous_end_time

        end_time_padded = subtitles.subs[-1].end + self.padding_milliseconds
        if subtitles.next_start_time and end_time_padded > subtitles.next_start_time:
            end_time_padded = subtitles.next_start_time

        return [start_time_padded, end_time_padded]


def add_effects(subtitles):
    effected_subs = SSAFile()
    for sub in subtitles:
        content = sub.plaintext.strip().replace('\n', ' ')
        time_per_syllable = (sub.end-sub.start)/syllables.estimate(content)
        current_time = sub.start
        current_index = 0
        for word in content.split(' '):
            sylls = syllables.estimate(word)
            sub_end_time = current_time + time_per_syllable*sylls
            current_index += len(word) if current_index == 0 else len(word) + 1
            text = content[:current_index] + '{\\alpha&HFF}' + content[current_index:]  # adds transparency
            effected_subs.append(SSAEvent(start=current_time, end=sub_end_time, text=text))
            current_time = sub_end_time
    return effected_subs


def trim(source, subs_filename, output, start, end):
    subprocess.run([
        'ffmpeg',
        '-ss', str(start),
        '-i', source,
        '-vf', 'ass=' + subs_filename,
        '-t', str(end - start),
        '-c:v', 'libx264',
        # '-async', '1',
        # '-an', # Removes audio
        output,
        '-n'
    ], check=True)


def find_trim_times(source, subtitles, min_start_time, max_end_time):

    video_manager = VideoManager([source])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    try:
        # Set downscale factor to improve processing speed (no args means default).
        video_manager.set_downscale_factor()
        x = FrameTimecode(timecode=min_start_time, fps=video_manager.get_framerate())
        y = FrameTimecode(timecode=max_end_time, fps=video_manager.get_framerate())
        video_manager.set_duration(start_time=x, end_time=y)
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(base_timecode)

        subs_start = FrameTimecode(timecode=str(subtitles[0].start), fps=video_manager.get_framerate())
        subs_end = FrameTimecode(timecode=str(subtitles[-1].end), fps=video_manager.get_framerate())

        trim_start = x
        trim_end = y
        for scene in enumerate(scene_list):
            timecodes = scene[1]
            start_frame = timecodes[0].get_frames()
            end_frame = timecodes[1].get_frames()
            if subs_start.get_frames() >= start_frame > trim_start.get_frames():
                trim_start = timecodes[0]
            if trim_end.get_frames() > end_frame >= subs_end.get_frames():
                trim_end = timecodes[1]

        trim_end = FrameTimecode(timecode=trim_end.get_frames() - 1, fps=video_manager.get_framerate())

    finally:
        video_manager.release()

    return [trim_start, trim_end]


def get_output_name(source, subtitles, output_format):
    out_path = os.path.dirname(os.path.abspath(source))
    no_new_lines = subtitles[0].plaintext.strip('\n').lower()[:30]
    with_dashes = re.sub('[^0-9A-z]+', '-', no_new_lines).strip('-')
    unique_output = with_dashes + '-' + ''.join(os.urandom(4).hex()) + output_format
    return os.path.join(out_path, unique_output)
