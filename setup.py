from setuptools import setup, find_packages

setup(
    name="catchery",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your production dependencies here
        # e.g., 'requests>=2.20.0',
    ],
    extras_require={
        "dev": [
            "ruff",
            "mypy",
            "pytest",
        ],
    },
    author="Enrico Fraccaroli",
    author_email="enrico.fraccaroli@univr.it",
    description="A python error handler. Catch exceptions and handle them gracefully.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Galfurian/catchery",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
