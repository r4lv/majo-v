#!/usr/bin/env python

from setuptools import find_packages, setup
import os
import re

setup_data = dict(
    name="majo_v",
    description="Mojave-like time aware wallpapers for all Macs",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=[
        "click>=6.0",
        "pyobjc-core>=4.0",
        "pendulum~=2.0",
        "rumps==0.2.2",
        "pathlib2;python_version<\"3.4\""
    ],
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": ["majo-v=majo_v:cli"]
    }
)


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    setup_data["long_description"] = "\n" + f.read()
    setup_data["long_description_content_type"] = "text/markdown"

with open(os.path.join(here, "{}.py".format(setup_data["name"]))) as f:
    content = f.read()
    for k in ["version", "author", "author_email", "url", "license"]:
        m = re.search("^__{}__ = \"(.*?)\"".format(k), content, re.MULTILINE)
        if not m:
            raise ValueError("cannot read '{}' from module file.".format(k))

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
