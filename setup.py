import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ndutils",
    version="0.1.3",
    description="zendriver utility functions for web crawling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rwiv/ndutils",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydantic>=2.11.7",
        "zendriver>=0.14.2",
    ],
)
