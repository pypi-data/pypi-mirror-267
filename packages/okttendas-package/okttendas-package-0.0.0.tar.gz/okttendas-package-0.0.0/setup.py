from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'A package including all Functions that Okttenda reuses.'

# Setting up
setup(
    name="okttendas-package",
    version=VERSION,
    author="Okttenda",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)