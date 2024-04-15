from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'SecLoad SDK package for Roblox Script Builder APIs.'

# Setting up
setup(
        name="SecLoadSDK", 
        version=VERSION,
        author="equsjd",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests_html', 'lxml_html_clean'],
        
        keywords=['roblox'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
        ]
)