"""
Installation script for satchmo-nogroth
"""

from setuptools import setup

setup(
    name = "satchmo-nogroth",
    packages = [
        "nogroth", 
        "nogroth.management", 
        "nogroth.management.commands",
        "nogroth.migrations"
    ],
    version = "0.1.3",
    description = "A tiered weight shipping module for Satchmo that is Administrative Area (i.e. state/province) aware",
    author = "Kevin Harvey",
    author_email = "kcharvey@gmail.com",
    maintainer = "Kevin Harvey",
    maintainer_email = "kcharvey@gmail.com",
    url = "https://github.com/kcharvey/satchmo-nogroth",
    download_url = "https://github.com/kcharvey/satchmo-nogroth/archive/master.zip",
    keywords = ["django", "satchmo", "shipping", "tiered weight", "by state"],
    platforms = ["Platform independant",],
    classifiers = [        
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",        
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        ],
    license = "BSD",
    long_description = "See https://github.com/kcharvey/satchmo-nogroth for isntallation instructions."
)
