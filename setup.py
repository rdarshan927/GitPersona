from setuptools import setup, find_packages

setup(
    name="gitpersona",
    version="0.1.0",
    description="Developer persona and analytics toolkit for GitHub profiles",
    packages=find_packages(exclude=("tests",)),
    install_requires=["requests"],
    entry_points={
        "console_scripts": ["gitpersona=gitpersona.cli:main"],
    },
)
