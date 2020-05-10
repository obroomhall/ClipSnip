# AutoGIF
## Overview
AutoGIF is a command line tool that can take just 2 arguments; a path to a video file, and a quote to search for. What it aims to return is a set of short, relevant clips from that file, like this:

```
quote="nicest" vid="Community.S01E01.1080p.BluRay.x264.mkv"
```
![Community](https://media.giphy.com/media/TFaDvUr4O9pR9jKz4q/giphy.gif)

## Key Features
* Subtitle sourcing and syncing
* Frame perfect scene extraction
* Simple usage

## Planned Features
* Subtitle customisation with fonts, sizes, colours, positions, etc.

## How it works
The pipeline used in AutoGIF is described below:
1. Identify media and find equivalent subtitles
2. Sync subtitles to the video using [subsync](https://github.com/smacke/subsync) to avoid offset issues
3. Search subtitles with [whoosh](https://github.com/mchaput/whoosh) to find candidates for extraction
4. Parse video file to find scene cuts nearby to the selected subtitles using [PySceneDetect](https://github.com/Breakthrough/PySceneDetect)
5. Extract clips and hardcode subtitles

## Development
A list of things experienced during the development of this project:
* PyScene detect was grabbing every frame in order to skip to a known point in the video, which was taking up significant processing time, so I [submitted a fix](https://github.com/Breakthrough/PySceneDetect/pull/163) to them which skips straight to the wanted frame
* More to come...
