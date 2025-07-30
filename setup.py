from setuptools import setup, find_packages

setup(
    name='catchery',
    version='0.0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your production dependencies here
        # e.g., 'requests>=2.20.0',
    ],
    extras_require={
        'dev': [
            'ruff',
            'mypy',
            'pytest',
        ],
    },
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    description='A short description of your project', # Replace with your project description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/catchery', # Replace with your project's GitHub URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
