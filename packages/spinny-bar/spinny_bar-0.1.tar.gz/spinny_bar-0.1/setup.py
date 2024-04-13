from setuptools import setup, find_packages

with open("README.md") as des:
    long_description = des.read()

setup(
    name="spinny_bar",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown"
)