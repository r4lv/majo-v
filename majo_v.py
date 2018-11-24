from pathlib import Path
import signal

from AppKit import NSScreen, NSWorkspace, NSApplication, NSObject
from Foundation import NSURL
import click
import rumps
import pendulum

__version__ = "0.3.2"
__author__ = "r4lv"
__author_email__ = "r4lv@peaxels.com"
__url__ = "https://github.com/r4lv/majo-v"
__license__ = "MIT"


def set_wallpaper_from_folder(folder, now=None):
    if now is None:
        now = pendulum.now()
    current_time_key = "{:HH_mm}".format(now)
    images_in_folder = {f.stem: f for f in Path(folder).glob("*.jpg")}
    all_keys = sorted(list(images_in_folder.keys()) + [current_time_key])
    pos_current = len(all_keys) - 1 - all_keys[::-1].index(current_time_key)
    u = NSURL.fileURLWithPath_(str(images_in_folder[all_keys[pos_current - 1]]))
    for s in NSScreen.screens():
        NSWorkspace.sharedWorkspace().setDesktopImageURL_forScreen_options_error_(u, s, None, None)

    try:
        return pendulum.parse(all_keys[pos_current + 1].replace("_", ":"), tz="local")
    except IndexError:  # fails when current image is the last for today
        return pendulum.parse(all_keys[0].replace("_", ":"), tz="local").add(days=1)


class MajoVApp(rumps.App):
    def __init__(self, folder):
        super().__init__("majo-v", menu=["set wallpaper now", None], quit_button="Quit majo-v",
                         icon=str(Path(__file__).parent.joinpath("menubar.tiff")), template=True)
        self.folder = folder
        self.next_run = pendulum.yesterday()
        rumps.Timer(callback=self.callback_timer, interval=15).start()

        _ = NSApplication.sharedApplication()  # noqa:F841, required to enable notif-center
        self.obsrv = type("r", (NSObject,), dict(spaceDidChange_=lambda s, n: self.set_now())).new()
        NSWorkspace.sharedWorkspace().notificationCenter().addObserver_selector_name_object_(
            self.obsrv, "spaceDidChange:", "NSWorkspaceActiveSpaceDidChangeNotification", None)

    @rumps.clicked("set wallpaper now")
    def set_now(self, _=None):
        self.next_run = set_wallpaper_from_folder(self.folder)

    def callback_timer(self, _):
        if pendulum.now() > self.next_run:
            self.set_now()


@click.command(options_metavar="[--version] [--gui] [--current-time 'HH:MM']")
@click.version_option(version=__version__, message="%(prog)s v%(version)s")
@click.option("-g", "--gui", is_flag=True, default=False,
              help="Start as menu bar app and update wallpaper automatically.")
@click.option("-t", "--current-time", default=None, metavar="'HH:MM'",
              help=("Overwrite time used for selecting the most fitting image."))
@click.argument("folder", type=click.Path(exists=True, resolve_path=True))
def cli(gui, current_time, folder):
    """
    Set the most fitting image from the given folder as wallpaper.

    FOLDER contains a set of jpg images, where the filenames are named after the time of the day
    where they should appear first, in the format 'HH_MM.jpg', e.g. '06_00.jpg' for an image which
    is to be displayed after 6am, '08_30.jpg' for an image displayed after 8:30, and so on.
    """
    if gui:
        signal.signal(signal.SIGINT, lambda signal, frame: rumps.quit_application())
        MajoVApp(folder).run()
    else:
        set_wallpaper_from_folder(folder, current_time and pendulum.parse(current_time, tz="local"))
