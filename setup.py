#!/usr/bin/env python

from setuptools import find_packages, setup
from pathlib import Path
import re

setup_data = dict(
    name="majo_v",
    description="Mojave-like time aware wallpapers for all Macs",
    python_requires=">=3.4.0",  # 'pathlib' introduced in 3.4
    install_requires=[
        "click~=7.0",
        "pyobjc-core~=5.1.1",
        "pendulum~=2.0.4",
        "rumps~=0.2.2"
    ],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": ["majo-v=majo_v:cli"]
    }
)


here = Path(__file__).parent.absolute()

with open(here / "README.md") as f:
    setup_data["long_description"] = "\n" + f.read()
    setup_data["long_description_content_type"] = "text/markdown"

with open(here / f"{setup_data['name']}.py") as f:
    content = f.read()
    for k in ["version", "author", "author_email", "url", "license"]:
        m = re.search(f"^__{k}__ = \"(.*?)\"", content, re.MULTILINE)
        if not m:
            raise ValueError(f"cannot read '{k}' from module file.")

        setup_data[k] = m.group(1)

setup(
    packages=find_packages(exclude=("tests",)),
    setup_requires=[
        "setuptools_git >= 0.3",
    ],
    include_package_data=True,
    zip_safe=False,
    **setup_data
)
