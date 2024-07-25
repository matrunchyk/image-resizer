from setuptools import setup

APP = ['gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['PIL', 'tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
