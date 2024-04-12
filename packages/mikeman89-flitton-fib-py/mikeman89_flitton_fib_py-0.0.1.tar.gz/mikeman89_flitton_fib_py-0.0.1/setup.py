from setuptools import setup, find_packages

import flitton_fib_py

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="mikeman89_flitton_fib_py",
    version="0.0.1",
    author="Michael Al Tork",
    author_email="michael.altork@gmail.com",
    description="Calculate Fibonacci number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikeman89/flitton-fib-py.git",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['fib-number = flitton_fib_py.cmd.fib_numb:fib_numb'],
    },
)
