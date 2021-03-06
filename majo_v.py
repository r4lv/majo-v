try:
    from pathlib import Path
except ImportError:  # python2
    from pathlib2 import Path
import signal

from AppKit import NSScreen, NSWorkspace, NSApplication, NSObject
from Foundation import NSURL
import click
import rumps
import pendulum

__version__ = "0.4.0"
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
    except IndexError:  # fails when current image is the last one for today
        return pendulum.parse(all_keys[0].replace("_", ":"), tz="local").add(days=1)


class MajoVApp(rumps.App):
    def __init__(self, folder):
        super(MajoVApp, self).__init__("majo-v", None, str(Path(__file__).parent / "menubar.tiff"),
                                       True, ["set wallpaper now", None], "Quit majo-v")
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


@click.command(options_metavar="[--version] [--no-icon|--once] [--current-time 'HH:MM']")
@click.version_option(version=__version__, message="%(prog)s v%(version)s")
@click.option("--no-icon", "mode", flag_value="faceless", default=False,
              help="Do not show the menu bar icon.")
@click.option("--once", "mode", flag_value="once", default=False,
              help="Set wallpaper and quit.")
@click.option("--current-time", default=None, metavar="'HH:MM'",
              help=("Overwrite time used for selecting the most fitting image."))
@click.argument("folder", type=click.Path(exists=True, resolve_path=True))
def cli(mode, current_time, folder):
    """
    Set the most fitting image from the given folder as wallpaper.

    FOLDER contains a set of jpg images, where the filenames are named after the time of the day
    where they should appear first, in the format 'HH_MM.jpg', e.g. '06_00.jpg' for an image which
    is to be displayed after 6am, '08_30.jpg' for an image displayed after 8:30, and so on.
    """
    if mode == "once":
        set_wallpaper_from_folder(folder, current_time and pendulum.parse(current_time, tz="local"))
    else:
        signal.signal(signal.SIGINT, lambda signal, frame: rumps.quit_application())
        if mode == "faceless":
            rumps.rumps.AppHelper.runEventLoop = rumps.rumps.AppHelper.runConsoleEventLoop
            rumps.rumps.NSApp.initializeStatusBar = lambda self: None
        MajoVApp(folder).run()
