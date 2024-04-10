import setuptools

VERSION = '0.0.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="punctuationstripper",
    version=VERSION,
    author="David Flanders",
    author_email="thedatadave@gmail.com",
    description="A package to strip punctuation from text via a file or a basic string.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheDataDave/punctuationstripper",
    keywords=['python', 'punctuation', 'text cleaning', 'data cleaning', 'NLP', 'string manipulation'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
    ],
)