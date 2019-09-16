import os

from setuptools import setup, find_packages

version = "0.2.1"

if os.environ.get('DEB', None):
    kwargs = {'data_files': [("/usr/bin/", ["files/gxenv"])]}
else:
    kwargs = dict()

setup(
    name="gxenv",
    version=version,
    author="GROOVE X Development Team",
    author_email="dev@groove-x.com",
    description="a GX-flavored venv wrapper",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["test*"]),
    test_suite="tests",
    extras_require={"dev": ["black"]},
    **kwargs,
)
