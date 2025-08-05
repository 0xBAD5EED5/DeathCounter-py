"""
Death Counter - Setup script for easy installation and distribution

This script allows the Death Counter to be installed as a Python package.
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="death-counter",
    version="1.0.0",
    author="0xBAD5EED5",
    description="Real-time death counter for FromSoftware games using OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/DeathCounter-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "death-counter-gui=src.death_counter_gui:main",
            "death-counter=src.death_counter:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.sh", "*.bat"],
    },
    keywords="game gaming fromsoft dark-souls elden-ring ocr death-counter",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/DeathCounter-py/issues",
        "Source": "https://github.com/YOUR_USERNAME/DeathCounter-py",
        "Documentation": "https://github.com/YOUR_USERNAME/DeathCounter-py#readme",
    },
)
