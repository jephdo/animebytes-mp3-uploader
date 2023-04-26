import re
import time

import click

from .animebytes import (
    check_completed,
    create_torrent,
    download_torrent,
    transcode_files,
)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    pass


@cli.command()
@click.argument("torrent")
@click.option("--transcode/--no-transcode", default=True)
def download(torrent, transcode, max_retries=10, sleep_time_sec=2):
    if isinstance(torrent, str) and torrent.startswith("http"):
        match = re.match(r"https://animebytes.tv/torrent/(\d*)/download/.*", torrent)
        if not match:
            raise click.BadParameter("Torrent must be an integer or a URL")
        torrent = match.groups()[0]
    try:
        torrent = int(torrent)
    except ValueError:
        raise click.BadParameter("Torrent must be an integer or a URL")

    infohash = download_torrent(torrent)
    click.echo(f"Downloaded torrent with infohash: {infohash}")

    if transcode:
        count = 0
        while True:
            if check_completed(infohash):
                click.echo("Torrent download complete")
                break
            if count > max_retries:
                raise click.ClickException("Torrent download timed out")
            time.sleep(sleep_time_sec)
            count += 1
        dst_path = transcode_files(infohash)
        click.echo(f"Transcoded files to: {dst_path}")
        outfile = create_torrent(dst_path)
        click.echo(f"Torrent file written to: {outfile}")


@cli.command()
@click.argument("infohash", type=str)
def transcode(infohash):
    dst_path = transcode_files(infohash)
    click.echo(f"Transcoded files to: {dst_path}")

    outfile = create_torrent(dst_path)
    click.echo(f"Torrent file written to: {outfile}")


if __name__ == "__main__":
    cli()
    cli()
