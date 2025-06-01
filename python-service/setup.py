#packaging 
from setuptools import setup, find_packages   # type: ignore
import re
import os

version_file = os.path.join("python_servicepkg", "__init__.py")  #extract version from __init__.py
with open(version_file, encoding="utf-8") as f:
    version_match = re.search(r'^__version__\s*=\s*["\'](.+)["\']', f.read(), re.M)
    if not version_match:
        raise RuntimeError("Unable to find __version__ in __init__.py")
    version = version_match.group(1)
setup(
    name='python-service',
    version=version, 
    packages=find_packages(),
    install_requires=[
        # production dependencies here 
    ],
    extras_require={
        'dev': [
            "python-semantic-release",
            "setuptools>=42",
            "wheel",
            "commitizen",
            "gitpython",
            "requests",
            "twine"
        ]
    },
    python_requires='>=3.6',
)
