# ClipSnip [![](https://img.shields.io/pypi/v/clipsnip.svg)](https://pypi.org/pypi/clipsnip/) [![](https://img.shields.io/pypi/pyversions/clipsnip.svg)](https://pypi.org/pypi/clipsnip/) [![](https://img.shields.io/pypi/status/clipsnip.svg)](https://pypi.org/pypi/clipsnip/)

ClipSnip is a command line tool that that automates the creation of GIFs from media files.


## Usage

Simple usage:
```
snip -q "nicest" -v "Community.S01E01.1080p.BluRay.x264.mkv"
```
Parameters:
* The quote to search for (`-q`)
* The video file to snip (`-v`)

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

2. Install ClipSnip with OpenCV
    ```
    pip install clipsnip[opencv]
    ```
   
    Otherwise, if you already have OpenCV
    ```
    pip install clipsnip
    ```


## Credits

* [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) for detecting start and end of scenes
* [ffsubsync](https://github.com/smacke/ffsubsync) for syncing subtitles to audio streams
* [ffmpeg](https://ffmpeg.org/) for being awesome
