# AutoTrim [![](https://img.shields.io/pypi/v/autotrim.svg)](https://pypi.org/pypi/autotrim/) [![](https://img.shields.io/pypi/pyversions/autotrim.svg)](https://pypi.org/pypi/autotrim/) [![](https://img.shields.io/pypi/status/autotrim.svg)](https://pypi.org/pypi/autotrim/)

AutoTrim is a command line tool that that automates the creation of GIFs from media files.


## Usage

Simple usage:
```
autotrim -q "nicest" -v "Community.S01E01.1080p.BluRay.x264.mkv"
```
Parameters:
* The quote to search for (`-q`)
* The video file to trim (`-v`)

output-1 | output-2
:---:|:---:
![Community](https://media.giphy.com/media/TFaDvUr4O9pR9jKz4q/giphy.gif) | ![Community2](https://media.giphy.com/media/SwTwbjka5sLMpxsuAt/giphy.gif)


## Key Features

* Media file identification
* Subtitle sourcing, syncing and searching
* Frame perfect scene extraction


## Installation

1. Ensure you have [ffmpeg](https://ffmpeg.org/) installed
    ```
    sudo apt-get install ffmpeg
    ```

2. Install AutoTrim with OpenCV
    ```
    pip install autotrim[opencv]
    ```
   
    Otherwise, if you already have OpenCV
    ```
    pip install autotrim
    ```


## Credits

* [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) for detecting start and end of scenes
* [ffsubsync](https://github.com/smacke/ffsubsync) for syncing subtitles to audio streams
* [ffmpeg](https://ffmpeg.org/) for being awesome
