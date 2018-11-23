from pathlib import Path
from datetime import datetime

from AppKit import NSScreen, NSWorkspace
from Foundation import NSURL
import click

from .__version__ import __version__


def _callback_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("majo-v v{}".format(__version__))
    ctx.exit()


def index_last(lst, key):
    """
    Like ``lst.index(key)``, but return the index of the last occurence instead of the first.
    """
    return len(lst) - 1 - lst[::-1].index(key)


def set_wallpaper(fn):
    """
    Set a wallpaper for every screen.

    Parameters
    ----------
    fn : str or Path

    """
    file_url = NSURL.fileURLWithPath_(str(Path(fn).absolute()))
    for screen in NSScreen.screens():
        NSWorkspace.sharedWorkspace().setDesktopImageURL_forScreen_options_error_(file_url, screen,
                                                                                  None, None)


@click.command()
@click.option("--version", is_flag=True, callback=_callback_version,
              expose_value=False, is_eager=True)
@click.option("-n", "--dry-run", is_flag=True, default=False)
@click.option("--current-time", default=None)
@click.argument("folder", type=click.Path(exists=True, file_okay=False, dir_okay=True,
                                          resolve_path=True))
def cli(dry_run, current_time, folder):
    if current_time is None:
        now = datetime.now()
        current_time = "{:%H_%M}".format(now)

    images_in_folder = {}
    for f in Path(folder).glob("*.jpg"):
        images_in_folder[f.stem] = f

    all_keys = sorted(list(images_in_folder.keys()) + [current_time])
    pos_current = index_last(all_keys, current_time)
    key_prev = all_keys[pos_current - 1]

    if dry_run:
        print("NOT loading wallpaper '{}' (dry-run mode)".format(images_in_folder[key_prev]))
    else:
        print("loading wallpaper '{}'".format(images_in_folder[key_prev]))
        set_wallpaper(images_in_folder[key_prev])


