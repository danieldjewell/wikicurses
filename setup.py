 #!/usr/bin/env python3

from setuptools import setup

import os.path
import sys
import warnings 

# Changed paths to remove absolutes

files_spec = [
        ('share/wikicurses', ['conf/wikicurses.conf.dist']),
        ('share/zsh/site-functions', ['zsh/_wikicurses']),
	('share/man/man1', ['docs/wikicurses.1']),
        ('share/man/man5', ['docs/wikicurses.conf.5'])
    ]

# Loop through and make the install relative to where we are now 
# Concept from github:ytdl-org/youtube-dl/setup.py
root = os.path.dirname(os.path.abspath(__file__))
data_files = []
for dirname, files in files_spec:
    resfiles = []
    for fn in files:
        if not os.path.exists(fn):
            warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
        else:
            resfiles.append(fn)
    data_files.append((dirname, resfiles))

setup(name='Wikicurses',
      version='1.4.1',
      description='A simple curses interface for accessing Wikipedia.',
      author='Ian D. Scott',
      author_email='ian@perebruin.com',
      license = "MIT",
      url='http://github.com/ids1024/wikicurses/',
      packages = ['wikicurses'],
      data_files=data_files,
      entry_points={'console_scripts': ['wikicurses = wikicurses.main:main']},
      install_requires = ['beautifulsoup4', 'lxml', 'urwid'],
      classifiers=[
          "Topic :: Internet :: WWW/HTTP",
          "Environment :: Console",
          "Environment :: Console :: Curses",
          "Operating System :: POSIX :: Linux",
          "Intended Audience :: End Users/Desktop",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3 :: Only",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License"
      ],
     )
