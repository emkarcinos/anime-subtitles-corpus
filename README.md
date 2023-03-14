# English anime subtitles corpus
This suite of scripts creates a language corpus from english anime subtitles.

## How it works
### Subtitles
Anime subtitles are created by the community and are shared to be used by everyone. They come in a variety of formats that are loaded and played alongside a video stream.

A typical subtitle file contains metadata, custom fonts, timestamps and text data. A library that parses the most common formats was used to extract dialogue text data.

#### Cleanup:
- Tags that are used to highlight pieces of text are removed
- Text in square bracers that is often used as sidenotes are dropped entirely
- Curly bracers are used in some formats to store additional metadata are also removed
- Lowercasing

As of the time of writing this doc, 34 215 subtitle were downloaded and used in the corpus itself. 

#### The corpus
Each entry is a piece of dialogue, either spoken by one character or a narrative description.
Subtitles also include opening / ending soundtrack, which lyrics are also included and translated.

Some of its cool stats:
- Size: 2G, 336MB compressed
- 29 532 187 lines in total

##### Examples:
`head -n 10 corpus.txt`:

```
sora ni aoi ryuusei
the blue comet in the sky...
yoru no unga o suberu you dane
...looks like it's slipping past the night
futari biru no mado kara
from the windows of our home...
tooku no machi o sagashite ita yo
...it looked like it was searching for a town far away
kanashii hitomi de
don't accuse me of love...
```

## Prequirements
- A suite of zip, rar and 7z executables on your mashine
- Python>3.9
- ~20G of disk space
## Setup
`pip install -r requirements.txt`

## Executing
### Getting the subtitles 
This tool crawls through https://www.kitsunekko.net in search of download links for each series subtitles.
It can be run either in parallel mode (default) or in a single threaded mode (make a change in `config.py` to switch) 

`python scrape.py`

Execution might take a while (~1hr)

### Extracting archives and processing all files
The following script extracts previously downloaded archives, parses each file and produces the corpus itself.
`python process.py`

Resulting files are `corpus.txt` (raw) and `corpus.txt.gz` (compressed).
