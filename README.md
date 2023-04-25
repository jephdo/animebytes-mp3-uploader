# AnimeBytes FLAC to MP3 V0 Uploader

## Requirements

1. For converting FLAC to MP3 [flac2mp3](https://github.com/robinbowes/flac2mp3)
2. Running qBittorrent instance
3. Python libraries: [torf](https://github.com/rndusr/torf), [qbittorrent-api](https://github.com/rmartin16/qbittorrent-api)

The `flac2mp3.pl` script is already included in the repository and depends on having `flac` and `lame` libraries installed

## Usage

```
$ python -m animebytes-uploader download https://animebytes.tv/torrent/<torrent_id>/download/<passkey>
```