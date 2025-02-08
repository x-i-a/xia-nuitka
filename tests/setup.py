from setuptools import setup, find_packages
from glob import glob
import os

binary_files = glob(f"xia_tests/**/*.so", recursive=True)
package_binary_files = []

setup(
    name="xia-tests",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Nuitka compiled package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your/repo",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "xia_tests": package_binary_files
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[],
)