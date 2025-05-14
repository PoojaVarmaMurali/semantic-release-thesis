from setuptools import setup, find_packages

setup(
    name='python-service',
    version='0.0.0',  # this will be overridden by semantic-release
    packages=find_packages(),
    install_requires=[
        # Your production dependencies go here
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
