from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up
setup(
    name="num-enumerator",
    version='0.0.4',
    author="Abhineet Raj",
    author_email="<abhineetraj01@outlook.com>",
    description=" This library helps to manipulate the 2d arrays. User can execute functions like addition, substraction, multiplication and other operations on square matrix and determinant.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords=['matrix', 'determinant','multiplication of matrix','division of matrix','addition of matrix','substraction of matrix','multiplication of determinant','division of determinant','addition of determinant','substraction of determinant'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)