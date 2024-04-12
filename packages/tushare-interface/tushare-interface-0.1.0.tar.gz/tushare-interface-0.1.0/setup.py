from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tushare-interface",
    version="0.1.0",
    author="polaritec",
    author_email="yuan.xin@polaritec.com",
    description="An interface encapsulated based on Tushare, which implements rate limiting and retry mechanisms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/polaritec/tushare-interface",
    packages=["tushare_interface"],
    tests_require=["unittest"],
    # List of dependencies
    install_requires=[
        "tushare>=1.4.5",
        "pandas>=2.2.1",
    ],
    python_requires=">=3.10",
    classifiers=[
        # Classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
