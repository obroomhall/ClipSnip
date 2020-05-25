# AutoTrim [![](https://img.shields.io/pypi/v/autotrim.svg)](https://pypi.org/pypi/autotrim/) [![](https://img.shields.io/pypi/pyversions/autotrim.svg)](https://pypi.org/pypi/autotrim/) [![](https://img.shields.io/pypi/status/autotrim.svg)](https://pypi.org/pypi/autotrim/)

## Overview
AutoTrim is a command line tool that can take just 2 arguments; a path to a video file, and a quote to search for, and aims to return a set of short, relevant clips from that file, like this:
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
1. Ensure you have [ffmpeg](https://ffmpeg.org/) installed.
    ```
    sudo apt-get install ffmpeg
    ```
   
2. (Optional) Install my fork of [PySceneDetect](https://github.com/obroomhall/PySceneDetect.git). Recommended as it fixes a seeking limitation in the original repo, resulting in significantly decreased runtime.
    ```
    pip install git+https://github.com/obroomhall/PySceneDetect.git
    ```
   
3. Install autotrim. If you do not have OpenCV already installed on your system, use:
    ```
    pip install autotrim[opencv]
    ```
   
    Otherwise, install with:
    ```
    pip install autotrim
    ```

## Major Credits
* [PySceneDetect](https://github.com/Breakthrough/PySceneDetect), for detecting start and end of scenes
* [ffsubsync](https://github.com/smacke/ffsubsync), for syncing subtitles to audio streams
* [ffmpeg](https://ffmpeg.org/), for being awesome
