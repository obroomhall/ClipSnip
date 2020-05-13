# AutoTrim
## Overview
AutoTrim is a command line tool that can take just 2 arguments; a path to a video file, and a quote to search for. What it aims to return is a set of short, relevant clips from that file, like this:

```
autotrim -q "nicest" -v "Community.S01E01.1080p.BluRay.x264.mkv"
```

output-1 | output-2
:---:|:---:
![Community](https://media.giphy.com/media/TFaDvUr4O9pR9jKz4q/giphy.gif) | ![Community2](https://media.giphy.com/media/SwTwbjka5sLMpxsuAt/giphy.gif)

## Key Features
* Media detection
* Subtitle sourcing and syncing
* Frame perfect scene extraction

## Installation
1. Install [ffmpeg](https://ffmpeg.org/).
```
sudo apt-get install ffmpeg
```
2. (Optional) Install my branch of [PySceneDetect](https://github.com/obroomhall/PySceneDetect.git). You should do this step because the [official repository](https://github.com/Breakthrough/PySceneDetect) has a limitation for skipping forward in video, which I was able to fix. So until they either update their code, or accept my [pull request](https://github.com/Breakthrough/PySceneDetect/pull/163), I recommend using my repository.
```
git clone https://github.com/obroomhall/PySceneDetect.git \
&& cd PySceneDetect \
&& python setup.py install \
&& cd .. \
&& rm -rf PySceneDetect
```
3. Install AutoTrim.
```
pip install autotrim
```

## Major Credits
* [PySceneDetect](https://github.com/Breakthrough/PySceneDetect), for detecting start and end of scenes
* [ffsubsync](https://github.com/smacke/ffsubsync), for syncing subtitles to audio streams
* [ffmpeg](https://ffmpeg.org/), for being awesome
