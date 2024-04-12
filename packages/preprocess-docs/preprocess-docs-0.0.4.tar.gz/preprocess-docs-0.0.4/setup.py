import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preprocess-docs",
    version="0.0.4",
    author="Eddy Jin",
    description="An open source document preprocessor for AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eddyjin1/preprocess",
    packages=setuptools.find_packages(),
    install_requires = [
      "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
