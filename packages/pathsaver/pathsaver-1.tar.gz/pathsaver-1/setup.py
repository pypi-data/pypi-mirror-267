from setuptools import setup, find_packages

setup(
    name='pathsaver',
    version='1.0',
    py_modules=['pathsaver'],
    install_requires=[
        'tabulate',
        'argcomplete',
    ],
    entry_points={
        'console_scripts': [
            'pathsaver = pathsaver:main',
        ],
    },
    author='Aditya Mohan',
    author_email='coding.traxicon16@gmail.com',
    description='A Python script for saving, listing, and managing directory paths.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TraXIcoN/pathsaver',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
