# AnimeBytes FLAC to MP3 V0 Uploader

## Requirements

1. For converting FLAC to MP3 [flac2mp3](https://github.com/robinbowes/flac2mp3)
2. Python libraries: [torf](https://github.com/rndusr/torf), [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api)

The `flac2mp3.pl` script is already included in the repository. It will require installing `flac` and `lame` libraries.

## Usage

```
$ python -m animebytes-uploader download https://animebytes.tv/torrent/<torrent_id>/download/<passkey>
```