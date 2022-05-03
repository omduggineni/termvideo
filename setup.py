from setuptools import setup

setup(
    name='termvideo',
    version='1.0',
    scripts=['termvideo.py'],
    license="LGPLv3",
    entry_points = {
        'console_scripts': ['termvideo=termvideo:main'],
    }
)