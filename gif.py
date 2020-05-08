import string
import subprocess
import srt
import re
import os
import random


tmp_dir = '.tmp/'
tmp_srt = os.path.join(tmp_dir, 'subs.srt')
tmp_ass = os.path.join(tmp_dir, 'subs.ass')
out_fmt = '.mp4'


def extract_gif(source, subtitle_list):

    for subtitle in subtitle_list:

        start = subtitle.start
        subtitle.start -= start
        subtitle.end -= start
        dur = subtitle.end - subtitle.start

        os.makedirs(tmp_dir, exist_ok=True)
        f = open(tmp_srt, "w")
        f.write(srt.compose([subtitle]))
        f.close()

        create_ass_res = subprocess.run('ffmpeg -i ' + tmp_srt + ' ' + tmp_ass + ' -n')
        if create_ass_res.returncode != 0:
            return create_ass_res.returncode
        os.remove(tmp_srt)

        out_path = os.path.dirname(os.path.abspath(source))
        output = os.path.join(
            out_path,
            get_output_name(subtitle_list[0])
            + '-'
            + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            + out_fmt
        )

        command = [
            'ffmpeg',
            '-ss', str(start),
            '-i', source,
            '-vf', 'ass=' + tmp_ass,
            '-t', str(dur),
            '-c:v', 'libx264',
            '-async', '1',
            '-an',
            output,
            '-n'
        ]
        print(command)

        res = subprocess.run(command)
        if res.returncode != 0:
            return res.returncode
        os.remove(tmp_ass)

    return res.returncode


def get_output_name(subtitle):
    no_new_lines = subtitle.content.strip('\n').lower()
    return re.sub('[^0-9A-z]+', '-', no_new_lines).strip('-')
