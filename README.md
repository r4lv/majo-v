# majo-v

[![release](https://img.shields.io/badge/release-v0.0.0-D19B62.svg)](https://github.com/r4lv/majo-v/releases)
![python version](https://img.shields.io/badge/python-3.4%E2%80%933.7-D19B62.svg)
![OS](https://img.shields.io/badge/OS-macOS%2010.11+-D19B62.svg?label=OS)


### Usage

``` text
Usage: majo-v [OPTIONS] FOLDER_WITH_IMAGES

Options:
  --version
  -n, --dry-run
  --current-time TEXT
  --help               Show this message and exit.
```

The `FOLDER_WITH_IMAGES` is a folder where each file is named like `HH_MM.jpg`, e.g. `06_00.jpg`, `08_00.jpg`, and so forth. You do not need to start with `00_00.jpg`, nor do you need to have a file for every hour (or minute…). *majo-v* automatically chooses the latest image available, based on the current time. You can override the current time by using the `--current-time HH_MM` option.

The `--dry-run` option does not actually change the wallpaper, just prints out the image it would use.