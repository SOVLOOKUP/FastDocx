import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastdocx",
    version="0.0.1",
    author="sovlookup",
    author_email="805408477@qq.com",
    description="use template to gen word everywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SOVLOOKUP/FastDocx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)