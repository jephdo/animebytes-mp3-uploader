import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    AB_PASSKEY = os.environ["AB_PASSKEY"]
    AB_SOURCE = "animebytes.tv"

    QBT_CONNECTION = {
        "host": "qbt-3.home.arpa",
        "port": 80,
    }
    QBT_FLAC_CATEGORY = "ab-flac"
    QBT_MP3_CATEGORY = "ab-mp3-v0"
    QBT_TAGS = "myupload"

    FLAC2MP3 = "./flac2mp3.pl"

    MEDIA_MOUNT_PATH = "/mnt/media"
    CREATED_TORRENT_LOCATION = "/mnt/media/downloads/tmp/ab-torrents/"


config = Config()
config.TRACKER_ANNOUNCE_URL = (
    f"https://tracker.animebytes.tv/{config.AB_PASSKEY}/announce"
)
