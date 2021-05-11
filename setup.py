import setuptools

with open("README.md", "r+", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastdocx",
    version="0.2.0",
    author="sovlookup",
    author_email="805408477@qq.com",
    description="use template to gen word everywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SOVLOOKUP/FastDocx",
    install_requires=[
        "python-docx",
        "trio",
        "httpx",
        "tqdm",
        "PyQt5"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)