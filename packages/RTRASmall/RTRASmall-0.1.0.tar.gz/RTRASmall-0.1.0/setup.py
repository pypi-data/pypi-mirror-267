from setuptools import setup, find_packages

setup(
    name="RTRASmall",                 # Name of your package
    version="0.1.0",                  # Version number
    author="udit Raj",               # Author's name
    author_email="udit_2312res708@iitp.ac.in",  # Author's email
    description="Python library for real-time data retrieval from the web",  # Brief description
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",  # Content type of long description
    url="https://github.com/yourusername/eternity",  # URL to the package repository
    license="MIT",                    # License type
    packages=find_packages(),         # List of packages to include (automatically finds all packages)
    install_requires=["requests"],    # Dependencies required for installation
    classifiers=[                     # Classifiers for categorizing your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

