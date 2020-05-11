import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autogif",
    version="0.0.1",
    author="Oliver Broomhall",
    author_email="obroomhall@gmail.com",
    description="Automated generation of GIF or GIFV from media files, using quotes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/obroomhall/AutoGIF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)