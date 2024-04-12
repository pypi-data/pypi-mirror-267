import pathlib
import os
import re
from setuptools import setup

ROOT = pathlib.Path(__file__).parent


with open(ROOT / "pywave/__init__.py", encoding="utf-8") as f:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ""
with open("README.rst") as f:
    readme = f.read()

setup(
    name="pywavee",
    author="PythonistaGuild, EvieePy, Timo",
    url="https://github.com/timoo4devv/pywave/",
    version=VERSION,
    packages=["pywave", "pywave.ext.spotify", "pywave.types"],
    license="MIT",
    description="A  robust and powerful Lavalink wrapper for py-cord and derivatives.",
    long_description=readme,
    include_package_data=True,
    install_requires=["aiohttp", "py-cord"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)