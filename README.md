# AutoGIF
## Overview
AutoGIF is a command line tool that can take just 2 arguments; a path to a video file, and a quote to search for. What it aims to return is a set of short, relevant clips from that file, like this:

```
autogif -q "nicest" -v "Community.S01E01.1080p.BluRay.x264.mkv"
```

output-1 | output-2
:---:|:---:
![Community](https://media.giphy.com/media/TFaDvUr4O9pR9jKz4q/giphy.gif) | ![Community2](https://media.giphy.com/media/SwTwbjka5sLMpxsuAt/giphy.gif)

## Key Features
* Subtitle sourcing and syncing
* Frame perfect scene extraction
* Simple usage

## Planned Features
* Optionally export most popular quotes automatically
* Subtitle customisation with fonts, sizes, colours, positions, etc.

## How it works
The pipeline used in AutoGIF is described below:
1. Identify media and find equivalent subtitles
2. Sync subtitles to the video using [subsync](https://github.com/smacke/subsync) to avoid offset issues
3. Search subtitles with [whoosh](https://github.com/mchaput/whoosh) to find candidates for extraction
4. Parse video file to find scene cuts nearby to the selected subtitles using [PySceneDetect](https://github.com/Breakthrough/PySceneDetect)
5. Extract clips and hardcode subtitles

## Frame perfect cuts
Nobody wants to see loose frames at the start or end of GIFs, they appear jarring and ruin the experience. To make sure never to have loose frames, I used [PySceneDetect](https://github.com/Breakthrough/PySceneDetect). Though, some jarring effect still occurs if the scene cuts too quickly after speech, or the end frame of the scene is very different from the start frame. If you have a GIF that you think contains loose frames, you can easily confirm it by using the following commands:
```
ffmpeg -i input.mp4 -vf "select=eq(n\,0)" -q:v 3 first.jpg
ffmpeg -sseof -3 -i input.mp4 -update 1 -q:v 1 last.jpg
```

## Development
A list of things experienced during the development of this project, this will be updated in time:
* PyScene detect was grabbing every frame in order to skip to a known point in the video, which was taking up significant processing time, so I [submitted a fix](https://github.com/Breakthrough/PySceneDetect/pull/163) to them which skips straight to the wanted frame
