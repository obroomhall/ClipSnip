import datetime
import os
import re
import subprocess
import string
from operator import itemgetter

import srt
from scenedetect.detectors import ContentDetector
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.scene_manager import SceneManager
from scenedetect.video_manager import VideoManager

from autotrim.config import tmp_dir


class GifExtractor:

    def __init__(self, padding_seconds=1.5):
        self.padding_seconds = padding_seconds
        self.output_format = '.mp4'

    def extract_gif(self, source, subtitles_list):

        for subtitles in subtitles_list:

            # gets an estimated start/end time from padding subtitles times
            [start_time_padded, end_time_padded] = get_padded_trim_times(subtitles, self.padding_seconds)

            # gets frame accurate start/end times for scene cuts
            [trim_start, trim_end] = find_trim_times(source, subtitles, start_time_padded, end_time_padded)

            output_filename = get_output_name(source, subtitles, self.output_format)

            offset = datetime.timedelta(seconds=trim_start.get_seconds())
            for sub in subtitles.subs:
                sub.start -= offset
                sub.end -= offset

            ass_filename = convert_srt_to_ass(subtitles)
            trim(source, ass_filename, output_filename, trim_start, trim_end)
            os.remove(ass_filename)


def convert_srt_to_ass(subtitles):
    srt_filename = os.path.join(tmp_dir, os.urandom(24).hex() + '.srt')
    ass_filename = os.path.join(tmp_dir, os.urandom(24).hex() + '.ass')
    with open(srt_filename, 'w') as tmp_srt:
        tmp_srt.write(srt.compose(subtitles.subs))
    subprocess.run([
        'ffmpeg',
        '-i', srt_filename,
        ass_filename,
        '-y'
    ], check=True)
    os.remove(srt_filename)
    return ass_filename


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


def get_padded_trim_times(subtitles, padding_seconds):

    padding = datetime.timedelta(seconds=padding_seconds)
    start_time_padded = subtitles.subs[0].start - padding
    if subtitles.previous_end_time and start_time_padded < subtitles.previous_end_time:
        start_time_padded = subtitles.previous_end_time

    end_time_padded = subtitles.subs[-1].end + padding
    if subtitles.next_start_time and end_time_padded > subtitles.next_start_time:
        end_time_padded = subtitles.next_start_time

    return [start_time_padded, end_time_padded]


def find_trim_times(source, subtitles, min_start_time, max_end_time):

    video_manager = VideoManager([source])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    try:
        # Set downscale factor to improve processing speed (no args means default).
        video_manager.set_downscale_factor()
        x = FrameTimecode(timecode=str(min_start_time), fps=video_manager.get_framerate())
        y = FrameTimecode(timecode=str(max_end_time), fps=video_manager.get_framerate())
        video_manager.set_duration(start_time=x, end_time=y)
        video_manager.start()
        scene_manager.detect_scenes(frame_source=video_manager)
        scene_list = scene_manager.get_scene_list(base_timecode)

        subs_start = FrameTimecode(timecode=str(subtitles.subs[0].start), fps=video_manager.get_framerate())
        subs_end = FrameTimecode(timecode=str(subtitles.subs[-1].end), fps=video_manager.get_framerate())

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
    no_new_lines = subtitles.subs[0].content.strip('\n').lower()[:30]
    with_dashes = re.sub('[^0-9A-z]+', '-', no_new_lines).strip('-')
    unique_output = with_dashes + '-' + ''.join(os.urandom(4).hex()) + output_format
    return os.path.join(out_path, unique_output)
