import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="preprocess-docs",
    version="0.0.6",
    author="Eddy Jin",
    description="An open source document preprocessor for AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="preprocess extract transform load parse documents html pdf images tables",
    url="https://github.com/eddyjin1/preprocess",
    packages=setuptools.find_packages(),
    install_requires = [
      "beautifulsoup4",
      "pdfminer.six",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.6',
)
