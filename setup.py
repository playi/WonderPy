import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WonderPy",
    version="0.0.1",
    author="Orion Elenzil",
    author_email="orion@makewonder.com",
    description="Python API for working with Wonder Workshop robots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/playi/WonderPy",
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Framework :: Robot Framework",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 2.7",
    ),
    # note that this requires WonderWorkshop's own github-hosted fork of Adafruit_BluefruitLE.
    #      see requirements.txt.
    install_requires=[ 'mock', 'svgpathtools', 'Adafruit_BluefruitLE'],
    keywords=['robots', 'dash', 'dot', 'cue', 'wonder workshop', 'robotics', 'sketchkit'],
    test_suite='test',
)



