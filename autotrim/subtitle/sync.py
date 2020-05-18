import os
import srt
import autotrim.subtitle.io as io
from ffsubsync import subsync

subsync_parser = subsync.make_parser()


def sync_subtitles(video_filename, subs_filename, dir_name):

    subtitles = io.read_subtitles(subs_filename)

    # subsync doesn't like some srt files from OpenSubtitles, so we
    # save them to our own file with utf-8 encoding
    encoded_subs_filename = os.path.join(dir_name, 'encoded.srt')
    with open(encoded_subs_filename, 'w') as f:
        f.write(srt.compose(subtitles))

    synced_subs_filename = os.path.join(dir_name, 'synced.srt')
    run_subsync(video_filename, encoded_subs_filename, synced_subs_filename)
    return synced_subs_filename


def run_subsync(reference, srtin, srtout):
    subsync_args = subsync_parser.parse_args([
        reference,
        '-i', srtin,
        '-o', srtout
    ])
    subsync.run(subsync_args)