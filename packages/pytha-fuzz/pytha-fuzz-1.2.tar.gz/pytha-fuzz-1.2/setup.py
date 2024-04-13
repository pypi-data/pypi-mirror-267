from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytha-fuzz",
    version="1.2",
    author="Parth Mishra",
    author_email="halfstackpgr@gmail.com",
    description="PYTHA is a Python-based directory fuzzer tool designed to aid in the discovery of hidden or sensitive directories and files on web servers. Originally developed by Shivang. Packed and moduled by the author.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivangmauryaa/pytha-fuzz",
    packages=["pytha"],
    entry_points={"console_scripts": ["fuzz=pytha.main:main"]},
    install_requires=["aiofiles", "colorama", "aiohttp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
