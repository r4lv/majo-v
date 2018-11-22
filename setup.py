#!/usr/bin/env python

from setuptools import find_packages, setup
from pathlib import Path

setup_data = dict(
    name="majo_v",
    python_requires=">=3.4.0",  # 3.4 introduced pathlib
    install_requires=[
        # pinned versions
        "click~=7.0",
        "pyobjc-core~=5.1.1"
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

with open(here / setup_data["name"] / "__version__.py") as f:
    about = {}
    exec(f.read(), about)  # noqa:S102


setup(
    version=about["__version__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    packages=find_packages(exclude=("tests",)),
    setup_requires=[
        "setuptools_git >= 0.3",
    ],
    include_package_data=True,
    zip_safe=False,
    **setup_data
)
