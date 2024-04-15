import os

from setuptools import setup

VERSION = "0.1.5"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="django-flasky",
    description="django-flasky is now nanodjango",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["nanodjango"],
    classifiers=["Development Status :: 7 - Inactive"],
)
