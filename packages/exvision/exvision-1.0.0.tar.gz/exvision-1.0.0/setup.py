from setuptools import setup, find_packages
with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="exvision",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    long_description=desc,
    long_description_content_type="text/markdown"
)