from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# Setting up
setup(
    name="aritrends",
    version='0.0.3',
    author="Abhineet Raj",
    author_email="<abhineetraj01@outlook.com>",
    description="This is a file processing library in python.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['docx2pdf', 'qrcode', 'pillow','py7zr','rarfile','PyPDF2'],
    keywords=['python', 'qrcode convertor', 'rar compressor', 'zip creator', '7z creator', 'image to pdf', 'file processing','pdf to docx'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)