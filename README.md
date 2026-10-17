# Instagram Reel Transcript Format Reference

A compact reference for choosing a transcript export and checking basic SubRip (`.srt`) timing syntax.

## Pick the file you need

| Format | Contains | Best for |
| --- | --- | --- |
| TXT | Plain spoken text | Reading, notes, search, editing copy |
| SRT | Ordered subtitle blocks with start and end timestamps | Video editors and timed subtitles |
| WebVTT (`.vtt`) | Timed text cues for WebVTT-compatible destinations | A platform that explicitly requests WebVTT |

A file extension does not confirm that the transcript is accurate. Read the text and compare a few timing ranges with the source video before publishing captions.

## Validate an SRT file

`validate_srt.py` performs a lightweight structure check. It detects malformed time ranges, end times before start times, non-sequential cue numbers, and missing text blocks.

```bash
python validate_srt.py examples/valid.srt
```

The script checks structure only. It cannot decide whether a subtitle matches the spoken audio.

## Files

- `format-selection.csv` — a machine-readable version of the format comparison.
- `validate_srt.py` — a dependency-free command-line SRT structure validator.
- `examples/valid.srt` — a small synthetic SRT example for testing.

For a public-Reel workflow and a route comparison, see the [Instagram Reel transcript format guide](https://igscript.com/instagram-reel-transcript-txt-srt-vtt).