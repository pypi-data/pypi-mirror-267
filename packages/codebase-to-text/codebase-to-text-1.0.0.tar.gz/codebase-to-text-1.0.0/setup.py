from setuptools import setup, find_packages
import sys
import os
print(os.getcwd())
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

setup(
    name="codebase-to-text",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["python-docx"],
    entry_points={
        "console_scripts": [
            "codebase-to-text = codebase_to_text.codebase_to_text:main",
        ]
    },
    author="Qaisar Tanvir",
    author_email="qaisartanvir.dev@gmail.com",
    description="A Python package to convert codebase to text",
    long_description="Converts a codebase (folder structure with files) into a single text file or a Microsoft Word document (.docx), preserving folder structure and file contents",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="codebase text conversion",
    url="https://github.com/QaisarRajput/codebase-to-text",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
