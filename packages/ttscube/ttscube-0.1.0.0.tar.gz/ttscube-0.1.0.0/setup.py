import setuptools


def parse_requirements(filename, session=None):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ttscube",
    version="0.1.0.0",

    author="Multiple authors",
    author_email="tiberiu44@gmail.com",
    description="Text-to-speech synthesis engine, based on end-to-end GAN training. Features: "
                "multilanguage, multispeaker, realtime CPU synthesis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiberiu44/TTS-Cube",
    packages=setuptools.find_packages()+['hifigan'],
    install_requires=parse_requirements('requirements.txt', session=False),
    classifiers=(
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
