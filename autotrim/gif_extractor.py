import string
import subprocess
import srt
import re
import os
import random
import datetime
from scenedetect.video_manager import VideoManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode


class GifExtractor:

    def __init__(self, dir_name, padding_seconds=1.5):
        self.dir_name = dir_name
        self.tmp_srt = os.path.join(dir_name, 'subs.srt')
        self.tmp_ass = os.path.join(dir_name, 'subs.ass')
        self.padding_seconds = padding_seconds
        self.output_format = '.mp4'

    def extract_gif(self, source, subtitle_list):

        for subtitles in subtitle_list:

            # gets an estimated start/end time from padding subtitles times
            [start_time_padded, end_time_padded] = get_padded_trim_times(subtitles, self.padding_seconds)

            # gets frame accurate start/end times for scene cuts
            [trim_start, trim_end] = find_trim_times(source, subtitles, start_time_padded, end_time_padded)

            output_filename = get_output_name(source, subtitles, self.output_format)

            offset = datetime.timedelta(seconds=trim_start.get_seconds())
            for sub in subtitles.subs:
                sub.start -= offset
                sub.end -= offset

            self.convert_srt_to_ass(subtitles)
            self.trim(source, output_filename, trim_start, trim_end)

    def convert_srt_to_ass(self, subtitles):

        f = open(self.tmp_srt, "w")
        f.write(srt.compose(subtitles.subs))
        f.close()

        subprocess.run([
            'ffmpeg',
            '-i', self.tmp_srt,
            self.tmp_ass,
            '-y'
        ], check=True)

        os.remove(self.tmp_srt)

    def trim(self, source, output, start, end):

        subprocess.run([
            'ffmpeg',
            '-ss', str(start),
            '-i', source,
            '-vf', 'ass=' + self.tmp_ass,
            '-t', str(end - start),
            '-c:v', 'libx264',
            # '-async', '1',
            # '-an',
            output,
            '-n'
        ], check=True)

        os.remove(self.tmp_ass)


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

    no_new_lines = subtitles.subs[0].content.strip('\n').lower()
    with_dashes = re.sub('[^0-9A-z]+', '-', no_new_lines).strip('-')

    return os.path.join(
        out_path,
        with_dashes
        + '-'
        + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        + output_format
    )
