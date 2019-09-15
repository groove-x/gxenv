from setuptools import setup, find_packages

version = "0.2.0"


setup(
    name="gxenv",
    version=version,
    author="GROOVE X Development Team",
    author_email="dev@groove-x.com",
    description="a GX-flavored venv wrapper",
    packages=find_packages(exclude=["test*"]),
    test_suite="tests",
    extras_require={"dev": ["black"]},
    data_files=[
        ("/usr/bin/", ["files/gxenv"]),
    ],
)
