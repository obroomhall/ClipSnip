import string
import subprocess
import srt
import re
import os
import random
import datetime
import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.detectors import ContentDetector
from scenedetect.scene_manager import SceneManager
from scenedetect.scene_detector import SceneDetector
from scenedetect.stats_manager import StatsManager
from scenedetect.frame_timecode import FrameTimecode

tmp_dir = '.tmp/'
tmp_srt = os.path.join(tmp_dir, 'subs.srt')
tmp_ass = os.path.join(tmp_dir, 'subs.ass')
out_fmt = '.mp4'


def extract_gif(source, subtitle_list):

    for subtitle in subtitle_list:

        padding = datetime.timedelta(seconds=1.5)
        start_time = subtitle.start - padding
        duration = (subtitle.end - subtitle.start) + 2 * padding

        video_manager = VideoManager([source])
        stats_manager = StatsManager()
        scene_manager = SceneManager(stats_manager)
        scene_manager.add_detector(ContentDetector())
        base_timecode = video_manager.get_base_timecode()

        try:
            # Set downscale factor to improve processing speed (no args means default).
            video_manager.set_downscale_factor()
            x = FrameTimecode(timecode=str(start_time), fps=video_manager.get_framerate())
            y = FrameTimecode(timecode=str(start_time + duration), fps=video_manager.get_framerate())
            video_manager.set_duration(start_time=x, end_time=y)
            video_manager.start()
            scene_manager.detect_scenes(frame_source=video_manager)
            scene_list = scene_manager.get_scene_list(base_timecode)

            subs_start = FrameTimecode(timecode=str(subtitle.start), fps=video_manager.get_framerate())
            subs_end = FrameTimecode(timecode=str(subtitle.end), fps=video_manager.get_framerate())

            trim_start = x
            trim_end = y
            for scene in enumerate(scene_list):
                timecodes = scene[1]
                start_frame = timecodes[0].get_frames()
                end_frame = timecodes[1].get_frames()
                if subs_start.get_frames() >= start_frame >= trim_start.get_frames():
                    trim_start = timecodes[0]
                if trim_end.get_frames() >= end_frame >= subs_end.get_frames():
                    trim_end = timecodes[1]

            trim_end = FrameTimecode(timecode=trim_end.get_frames()-1, fps=video_manager.get_framerate())

        finally:
            video_manager.release()

        out_path = os.path.dirname(os.path.abspath(source))
        output_filename = os.path.join(
            out_path,
            get_output_name(subtitle)
            + '-'
            + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            + out_fmt
        )

        offset = datetime.timedelta(seconds=trim_start.get_seconds())
        subtitle.start -= offset
        subtitle.end -= offset

        os.makedirs(tmp_dir, exist_ok=True)
        f = open(tmp_srt, "w")
        f.write(srt.compose([subtitle]))
        f.close()

        subprocess.run(
            'ffmpeg -i ' + tmp_srt + ' ' + tmp_ass + ' -n',
            check=True
        )
        os.remove(tmp_srt)

        subprocess.run([
            'ffmpeg',
            '-ss', str(trim_start),
            '-i', source,
            '-vf', 'ass=' + tmp_ass,
            '-t', str(trim_end - trim_start),
            '-c:v', 'libx264',
            '-async', '1',
            '-an',
            output_filename,
            '-n'
        ], check=True)
        os.remove(tmp_ass)


def get_output_name(subtitle):
    no_new_lines = subtitle.content.strip('\n').lower()
    return re.sub('[^0-9A-z]+', '-', no_new_lines).strip('-')
