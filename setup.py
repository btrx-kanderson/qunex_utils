import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qunex_utils-btrx-kanderson",
    version="0.0.1",
    author="Kevin Anderson",
    author_email="kevin.anderson@neumoratx.com",
    description="QUNEX utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/btrx-kanderson/qunex_utils",
    project_urls={
        "Bug Tracker": "https://github.com/btrx-kanderson/qunex_utils",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "qunex_utils"},
    packages=setuptools.find_packages(where="qunex_utils"),
    python_requires=">=3.6",
)