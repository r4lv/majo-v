from pathlib import Path
import signal

from AppKit import NSScreen, NSWorkspace
from Foundation import NSURL
import click
import rumps
import pendulum

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


def set_wallpaper_from_folder(folder, current_time_key, dry_run=False):
    images_in_folder = {f.stem: f for f in Path(folder).glob("*.jpg")}
    all_keys = sorted(list(images_in_folder.keys()) + [current_time_key])
    pos_current = index_last(all_keys, current_time_key)
    key_prev = all_keys[pos_current - 1]

    if dry_run:
        print("NOT loading wallpaper '{}' (dry-run mode)".format(images_in_folder[key_prev]))
    else:
        set_wallpaper(images_in_folder[key_prev])

    return all_keys[pos_current + 1]


class MajoVApp(rumps.App):
    def __init__(self, folder):
        super().__init__("majo-v")
        self.folder = folder
        self.next_run = pendulum.now() - pendulum.Duration(hours=1)

        self.menu = ["set now"]
        rumps.Timer(callback=self.callback_timer, interval=15).start()

    @rumps.clicked("set now")
    def action_set_now(self, _=None, current_time_key=None):
        if current_time_key is None:
            current_time_key = "{:HH_mm}".format(pendulum.now())
        next_key = set_wallpaper_from_folder(self.folder, current_time_key)
        self.next_run = pendulum.parse(next_key.replace("_", ":"))
        if self.next_run < pendulum.now():
            self.next_run += pendulum.Duration(days=1)

    def callback_timer(self, _):
        now = pendulum.now()
        if now > self.next_run:
            self.action_set_now(current_time_key="{:HH_mm}".format(now))


@click.command(options_metavar="[--version] [--dry-run|--gui] [--current-time 'HH_MM']")
@click.option("--version",
              is_flag=True, callback=_callback_version, expose_value=False, is_eager=True,
              help="show version information (majo-v v{})".format(__version__))
@click.option("-n", "--dry-run", "mode", flag_value="dry-run", default=False,
              help="do nothing, just show which wallpaper would be set")
@click.option("-g", "--gui", "mode", flag_value="gui", default=False,
              help="start menu bar app and update wallpaper automatically")
@click.option("--current-time", "current_time_key", default=None, metavar="'HH_MM'",
              help=("Overwrite current time used for selecting the most fitting image."))
@click.argument("folder",
                type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def cli(mode, current_time_key, folder):
    """
    Set the most fitting image from the given folder as wallpaper.

    FOLDER contains a set of jpg images, where the filenames are named after the time of the day
    where they should appear first, in the format 'HH_MM.jpg', e.g. '06_00.jpg' for an image which
    is to be displayed after 6am, '08_30.jpg' for an image displayed after 8:30, and so on.

    """
    if current_time_key is None:
        current_time_key = "{:HH_mm}".format(pendulum.now())
    if mode == "gui":
        signal.signal(signal.SIGINT, lambda signal, frame: rumps.quit_application())
        MajoVApp(folder).run()
    elif mode == "dry-run":
        set_wallpaper_from_folder(folder, current_time_key, dry_run=(mode == "dry-run"))
