# majo-v

[![release](https://img.shields.io/badge/release-v0.2.2-D19B62.svg)](https://github.com/r4lv/majo-v/releases)
![python version](https://img.shields.io/badge/python-3.4%E2%80%933.7-D19B62.svg)
![OS](https://img.shields.io/badge/OS-macOS%2010.11+-D19B62.svg?label=OS)

Have you seen the amazing dynamic wallpapers on the new macOS 10.14 Mojave? Mojave calculates the position of the sun for your current time and location, compares them to the 16 images inside `Mojave (Dynamic).heic` and displays the one closest to your constellation as wallpaper.

*majo-v* is a proof of concept to achieve the same, on all Macs, in ~100 lines of python.


## Installation

The recommended way of installing *majo-v* is with [pipsi](https://github.com/mitsuhiko/pipsi), but you can also use pip:

``` bash
pipsi install git+https://github.com/r4lv/majo-v#egg=majo-v
# or
pip3 install git+https://github.com/r4lv/majo-v#egg=majo-v
```

Note that *majo-v* requires python 3.4+.


## Usage

To use *majo-v*, you need a folder with a bunch of images inside. You can put there as many as you want (e.g. the [original 16 images from macOS Mojave](https://technastic.com/macos-mojave-dynamic-wallpapers/)), as long as you rename the files based on the *time of the day they should appear first*, in the format `HH_MM.jpg`, e.g. `06_00.jpg` for an image which is to be displayed after 6am, `08_30.jpg` for an image displayed after 8:30, and so on. You then pass the folder as command line argument to *majo-v*, which chooses the most fitting image, and sets it as wallpaper on all your screens.

``` text
Usage: majo-v [--version] [--dry-run|--gui] [--current-time 'HH_MM'] FOLDER

  Set the most fitting image from the given folder as wallpaper.

  FOLDER contains a set of jpg images, where the filenames are named after
  the time of the day where they should appear first, in the format
  'HH_MM.jpg', e.g. '06_00.jpg' for an image which is to be displayed after
  6am, '08_30.jpg' for an image displayed after 8:30, and so on.

Options:
  --version               show version information (majo-v v0.1.0)
  -n, --dry-run           do nothing, just show which wallpaper would be set
  -g, --gui               start menu bar app and update wallpaper automatically
  --current-time 'HH_MM'  Overwrite current time used for selecting the most
                          fitting image. Formatted like 'HH_MM'.
  --help                  Show this message and exit.
```

- by default, *majo-v* sets the wallpaper and exits. For a more Mojave-like experience, start *majo-v* with the `--gui` switch, which starts a menu bar app. The menu bar app watches the current time in the background, and updates the wallpaper whenever necessary. Use `&` to detach *majo-v* from your terminal:
   ``` bash
   majo-v --gui ~/Pictures/Mojave-Wallpaper &
   ```
- The `--dry-run` option does not actually change the wallpaper, just prints out the image it would use.
- You can override the current time by using the `--current-time HH_MM` option, to force a specific wallpaper. Useful in combination with `--dry-run`, to check what *majo-v* does.



## Internals

#### dependencies

*majo-v* depends on

- [click](https://click.palletsprojects.com), for the command line interface
- [pyobjc-core](https://pythonhosted.org/pyobjc/), for calling the macOS APIs
- [rumps](https://github.com/jaredks/rumps), for the menu bar interface
- [pendulum](https://pendulum.eustace.io), for handling date and time


#### (no) HEIC support

MacOS 10.14 Mojave's dynamic desktop feature uses single `.heic` files which contain a sequence of 16 images, together with metadata (altitude & azimuth of the sun in every image, and index of the default *dark* and *light* images when dynamic mode is disabled). I found no way of extracting the images on macOS version before Mojave (metadata can be extracted with 10.13 High Sierra), so you sadly cannot use `.heic` files with *majo-v*

#### (no) sun position calculation

This would be quite feasable, but I think the gain is little. Just rename your files in winter, so that the sunrise matches again ;)


## Further Reading

- [pysolar](https://github.com/pingswept/pysolar) could be used to calculate the current sun position
- [xtai/mojave-dynamic-heic](https://github.com/xtai/mojave-dynamic-heic) also has the extracted jpg from `Mojave (Dynamic).heic`
- [nshipster.com](https://nshipster.com/macos-dynamic-desktop/) has a nice nerdy article about dynamic wallpapers, CoreGraphics and HEIC. They also implemented a [solar position calculation](https://github.com/NSHipster/DynamicDesktop/blob/master/SolarPosition.playground/Sources/SolarPosition.swift) in Swift
- [pipwerks/OS-X-Wallpaper-Changer](https://github.com/pipwerks/OS-X-Wallpaper-Changer/) does something similar, but with applescript and just 6 wallpapers/day
- [sindresorhus/macos-wallpaper](https://github.com/sindresorhus/macos-wallpaper/blob/master/Sources/wallpaper/Wallpaper.swift) has some more sophisticated handling of `NSWorkspace.shared.setDesktopImageURL` and companions
