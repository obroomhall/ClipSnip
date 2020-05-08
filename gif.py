import subprocess


def extract_gif():
    source = 'test/Community.S01E01.1080p.BluRay.x264-YELLOWBiRD.mkv'
    ass = 'test/1952727133.ass'
    output = 'test/out.mp4'

    command = [
        'ffmpeg',
        '-ss', '00:01:03.43',
        '-i', source,
        '-vf', 'ass=' + ass,
        '-t', '2.73',
        '-c:v', 'libx264',
        '-async', '1',
        '-an',
        output,
        '-y'
    ]

    subprocess.run(command)
    print(command)
