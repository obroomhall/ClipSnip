import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='clipsnip',
    version='0.0.20',
    packages=setuptools.find_packages(),
    url='https://github.com/obroomhall/clipsnip',
    author='Oliver Broomhall',
    author_email='obroomhall@gmail.com',
    description='Automated extraction of short clips from media files, using quotes.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'snip = clipsnip.__main__:main'
        ],
    },
    install_requires=[
        'pysubs2',
        'python-opensubtitles',
        'whoosh',
        'tmdbsimple',
        'scenedetect[opencv-headless]',
        'ffsubsync',
        'wheel',
        'syllables'
    ],
    python_requires='>=3.5, <4',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    keywords='ffmpeg trim subtitles gif gifv video media tv film movie clip',
)
