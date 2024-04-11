from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'SecLoad SDK package for Roblox Script Builder APIs.'

# Setting up
setup(
        name="SecLoadSDK", 
        version=VERSION,
        author="equsjd",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['roblox'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)