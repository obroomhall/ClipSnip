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

Output:

<p align="center">
  <img src="https://media.giphy.com/media/TFaDvUr4O9pR9jKz4q/giphy.gif" width="400" />
  <img src="https://media.giphy.com/media/SwTwbjka5sLMpxsuAt/giphy.gif" width="400" />
</p>

## Key Features

* Media file identification
* Subtitle sourcing, syncing and searching
* Frame perfect scene extraction


## Installation

```
sudo apt-get install ffmpeg
pip install clipsnip
```


## Credits

* [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) for detecting start and end of scenes
* [ffsubsync](https://github.com/smacke/ffsubsync) for syncing subtitles to audio streams
* [ffmpeg](https://ffmpeg.org/) for being awesome
