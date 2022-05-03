from setuptools import setup

setup(
    name='termvideo',
    version='1.0.1',
    scripts=['termvideo.py'],
    author='Om Duggineni',
    install_requires=['numpy', 'opencv-python'],
    license="LGPLv3",
    entry_points = {
        'console_scripts': ['termvideo=termvideo:main'],
    }
)