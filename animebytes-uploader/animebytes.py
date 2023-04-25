from io import BytesIO
from pathlib import Path

import requests
import torf
import os
from qbittorrentapi import Client

from .config import config


def check_completed(infohash: str) -> bool:
    with Client(**config.QBT_CONNECTION) as client:
        info = client.torrents_info(torrent_hashes=infohash)
        assert len(info) == 1, "No torrent found with infohash: f{infohash}"
    return info[0].progress == 1


def download_torrent(torrent_id: int) -> str:
    download_url = (
        f"https://animebytes.tv/torrent/{torrent_id}/download/{config.AB_PASSKEY}"
    )
    response = requests.get(download_url)
    torrent_file = response.content
    torrent = torf.Torrent.read_stream(BytesIO(torrent_file))

    with Client(**config.QBT_CONNECTION) as client:
        print("Downloading torrent file...")
        client.torrents_add(
            torrent_files=torrent_file, category=config.QBT_FLAC_CATEGORY
        )

    return torrent.infohash


def transcode_files(infohash: str) -> Path:
    assert check_completed(infohash), "Torrent is not complete"
    with Client(**config.QBT_CONNECTION) as client:
        info = client.torrents_info(torrent_hashes=infohash)
        assert len(info) == 1, "No torrent found with infohash: f{infohash}"
        content_path = info[0].content_path
        content_path = content_path[1:]  # strip leading slash

    dst_path = config.MEDIA_MOUNT_PATH / Path(
        content_path.replace(config.QBT_FLAC_CATEGORY, config.QBT_MP3_CATEGORY)
        .replace("[48-24]", "[MP3 V0]")
        .replace("24bit FLAC", "MP3 V0")
    )

    if "flac" in dst_path.name.lower():
        dst_path = dst_path.with_name(
            dst_path.name.replace("flac", "mp3 v0").replace("FLAC", "MP3 V0")
        )

    dst_path.mkdir(parents=True, exist_ok=True)
    src_path = config.MEDIA_MOUNT_PATH / Path(content_path)

    for file in src_path.iterdir():
        if file.suffix == ".flac":
            continue
        try:
            os.link(file, dst_path / file.name)
            print(f"COPY: {file.name}")
        except FileExistsError:
            continue
    cmd = f'{config.FLAC2MP3} --preset=V0 --quiet "{src_path}" "{dst_path}"'
    print(f"Running: '{cmd}'")
    os.system(cmd)
    return dst_path


def create_torrent(dst_path: Path) -> Path:
    torrent = torf.Torrent(path=dst_path, trackers=[config.TRACKER_ANNOUNCE_URL])
    torrent.private = True
    torrent.source = config.AB_SOURCE
    torrent.generate()
    outfile = config.CREATED_TORRENT_LOCATION / Path(
        f"[AnimeBytes]{torrent.name}.torrent"
    )
    torrent.write(outfile, overwrite=True)

    with Client(**config.QBT_CONNECTION) as client:
        client.torrents_add(
            torrent_files=outfile,
            category=config.QBT_MP3_CATEGORY,
            tags=config.QBT_TAGS,
        )
        print("Torrent added to QBT")
    return outfile
