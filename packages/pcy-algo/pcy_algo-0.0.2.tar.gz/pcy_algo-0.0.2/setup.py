from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pcy_algo',
    version='0.0.2',
    description='PCY implementation in association rule mining',
    author= 'Murali B',
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['association rule mining','apriori algorithm','data mining'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['pcy_algo'],
    package_dir={'':'src'},
    install_requires = [
        'pandas',
    ]
)