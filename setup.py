import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='autotrim',
    version='0.0.9',
    packages=setuptools.find_packages(),
    url='https://github.com/obroomhall/autotrim',
    author='Oliver Broomhall',
    author_email='obroomhall@gmail.com',
    description='Automated extraction of short clips from media files, using quotes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'autotrim = autotrim.__main__:main'
        ],
    },
    install_requires=[
        'srt',
        'python-opensubtitles',
        'whoosh',
        'tmdbsimple',
        'scenedetect[progress_bar]',
        'ffsubsync',
    ],
    extras_require={
        'opencv': ['opencv-python'],
    },
    python_requires='>=3.5, <=3.8'
)
