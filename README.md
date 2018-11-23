# majo-v

[![release](https://img.shields.io/badge/release-v0.2.0-D19B62.svg)](https://github.com/r4lv/majo-v/releases)
![python version](https://img.shields.io/badge/python-3.4%E2%80%933.7-D19B62.svg)
![OS](https://img.shields.io/badge/OS-macOS%2010.11+-D19B62.svg?label=OS)

Have you seen the amazing dynamic wallpapers on the new macOS 10.14 Mojave? Mojave calculates the position of the sun for your current time and location, compares them to the 16 images inside `Mojave (Dynamic).heic` and displays the one closest to your constellation as wallpaper.

*majo-v* is a proof of concept to achieve the same, on all Macs, in ~50 lines of python.


### installation

Use [pipsi](https://github.com/mitsuhiko/pipsi) (or `pip`) to install the latest version:

``` bash
pipsi install git+https://github.com/r4lv/majo-v#egg=majo-v
```

Note that *majo-v* requires python 3.4+, and that pip(si) install the dependencies [click](https://click.palletsprojects.com) and [pyobjc-core](https://pythonhosted.org/pyobjc/) automatically.



### Usage

To use *majo-v*, you need a folder with a bunch of images inside. You can put there as many as you want (e.g. the [original 16 images from macOS Mojave](https://technastic.com/macos-mojave-dynamic-wallpapers/)), as long as you rename the files based on the *time of the day they should appear first*, in the format `HH_MM.jpg`, e.g. `06_00.jpg` for an image which is to be displayed after 6am, `08_30.jpg` for an image displayed after 8:30, and so on. You then pass the folder as command line argument to *majo-v*, which chooses the most fitting image, and sets it as wallpaper on all your screens.

``` text
Usage: majo-v [OPTIONS] FOLDER_WITH_IMAGES

Options:
  --version
  -n, --dry-run
  --current-time HH_MM
  --help               Show this message and exit.
```

- You can override the current time by using the `--current-time HH_MM` option, to force a specific wallpaper.
- The `--dry-run` option does not actually change the wallpaper, just prints out the image it would use.



### Further Reading

- [pysolar](https://github.com/pingswept/pysolar) could be used to 
- the extracted jpg from the `Mojave (Dynamic).heic` are also on [GitHub](https://github.com/xtai/mojave-dynamic-heic)
- [pipwerks/OS-X-Wallpaper-Changer](https://github.com/pipwerks/OS-X-Wallpaper-Changer/) does something similar, but with applescript and just 6 wallpapers/day
- [nshipster.com](https://nshipster.com/macos-dynamic-desktop/) has a nice nerdy article about dynamic wallpapers, CoreGraphics and HEIC. They also implemented a [solar position calculation](https://github.com/NSHipster/DynamicDesktop/blob/master/SolarPosition.playground/Sources/SolarPosition.swift) in Swift
- [sindresorhus/macos-wallpaper](https://github.com/sindresorhus/macos-wallpaper/blob/master/Sources/wallpaper/Wallpaper.swift) has some more sophisticated handling of `NSWorkspace.shared.setDesktopImageURL` and companions