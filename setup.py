from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ssml-maker",
    version="0.1.0",
    author="Kevin Sallée",
    author_email="kevin.sallee@gmail.com",
    description="A Python library for building SSML (Speech Synthesis Markup Language) documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ssml-maker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
    ],
    python_requires=">=3.7",
    install_requires=[],
    test_requires=["pytest"],
)
