from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '1.0.0' 
DESCRIPTION = 'SecLoad SDK package for Roblox Script Builder APIs.'

# Setting up
setup(
        name="SecLoad", 
        version=VERSION,
        author="equsjd",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        license_files = ('license.txt',),
        packages=find_packages(),
        install_requires=['requests_html', 'lxml_html_clean'],
        
        keywords=['roblox'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3",
        ]
)