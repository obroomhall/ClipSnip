from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='autogif',
    version='0.1.13',
    packages=['tests', 'autogif'],
    url='https://github.com/obroomhall/AutoGIF',
    license='Apache 2.0',
    author='Oliver Broomhall',
    author_email='obroomhall@gmail.com',
    description='Automated generation of GIF or GIFV from media files, using quotes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': ['autogif=autogif.main:main'],
    },
    install_requires=[
        'wheel',
        'srt',
        'python-opensubtitles',
        'whoosh',
        'tmdbsimple',
        'scenedetect[opencv,progress_bar]',
        'parse-torrent-name',
        'ffsubsync'
    ]
)
