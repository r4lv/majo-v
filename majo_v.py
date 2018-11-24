from pathlib import Path
import signal

from AppKit import NSScreen, NSWorkspace, NSApplication, NSObject
from Foundation import NSURL
import click
import rumps
import pendulum

__version__ = "0.3.1"
__author__ = "r4lv"
__author_email__ = "r4lv@peaxels.com"
__url__ = "https://github.com/r4lv/majo-v"
__license__ = "MIT"


def _cb_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("majo-v v{}".format(__version__))
    ctx.exit()


def set_wallpaper_from_folder(folder, current_time_key=None, dry_run=False):
    if current_time_key is None:
        current_time_key = "{:HH_mm}".format(pendulum.now())
    images_in_folder = {f.stem: f for f in Path(folder).glob("*.jpg")}
    all_keys = sorted(list(images_in_folder.keys()) + [current_time_key])
    pos_current = len(all_keys) - 1 - all_keys[::-1].index(current_time_key)
    key_prev = all_keys[pos_current - 1]

    if dry_run:
        print("NOT loading wallpaper '{}' (dry-run mode)".format(images_in_folder[key_prev]))
    else:
        url = NSURL.fileURLWithPath_(str(images_in_folder[key_prev]))
        for screen in NSScreen.screens():
            NSWorkspace.sharedWorkspace().setDesktopImageURL_forScreen_options_error_(
                url, screen, None, None)

    return all_keys[pos_current + 1]


class SpaceChangeDelegate(NSObject):
    def activeSpaceDidChange_(self, notif):
        self.callback()


class MajoVApp(rumps.App):
    def __init__(self, folder):
        super().__init__("majo-v", menu=["set wallpaper now", None], quit_button="Quit majo-v",
                         icon=str(Path(__file__).parent.joinpath("menubar.tiff")), template=True)
        self.folder = folder
        self.next_run = pendulum.now() - pendulum.Duration(hours=1)
        rumps.Timer(callback=self.callback_timer, interval=15).start()

        nsapplication = NSApplication.sharedApplication()  # noqa:F841
        self.scd = SpaceChangeDelegate.new()  # needs to be `self.`!
        self.scd.callback = self.action_set_now
        NSWorkspace.sharedWorkspace().notificationCenter().addObserver_selector_name_object_(
            self.scd, "activeSpaceDidChange:", "NSWorkspaceActiveSpaceDidChangeNotification", None)

    @rumps.clicked("set wallpaper now")
    def action_set_now(self, _=None, current_time_key=None):
        next_key = set_wallpaper_from_folder(self.folder, current_time_key)
        self.next_run = pendulum.parse(next_key.replace("_", ":"))
        if self.next_run < pendulum.now():
            self.next_run += pendulum.Duration(days=1)

    def callback_timer(self, _):
        if pendulum.now() > self.next_run:
            self.action_set_now()


@click.command(options_metavar="[--version] [--dry-run|--gui] [--current-time 'HH_MM']")
@click.option("--version", is_flag=True, callback=_cb_version, expose_value=False, is_eager=True,
              help="Show version information. (majo-v v{})".format(__version__))
@click.option("-n", "--dry-run", "mode", flag_value="dry-run", default=False,
              help="Do nothing, just show which wallpaper would be set.")
@click.option("-g", "--gui", "mode", flag_value="gui", default=False,
              help="Start as menu bar app and update wallpaper automatically.")
@click.option("--current-time", "current_time_key", default=None, metavar="'HH_MM'",
              help=("Overwrite time used for selecting the most fitting image."))
@click.argument("folder", type=click.Path(exists=True, resolve_path=True))
def cli(mode, current_time_key, folder):
    """
    Set the most fitting image from the given folder as wallpaper.

    FOLDER contains a set of jpg images, where the filenames are named after the time of the day
    where they should appear first, in the format 'HH_MM.jpg', e.g. '06_00.jpg' for an image which
    is to be displayed after 6am, '08_30.jpg' for an image displayed after 8:30, and so on.
    """
    if mode == "gui":
        signal.signal(signal.SIGINT, lambda signal, frame: rumps.quit_application())
        MajoVApp(folder).run()
    else:
        set_wallpaper_from_folder(folder, current_time_key, dry_run=(mode == "dry-run"))
