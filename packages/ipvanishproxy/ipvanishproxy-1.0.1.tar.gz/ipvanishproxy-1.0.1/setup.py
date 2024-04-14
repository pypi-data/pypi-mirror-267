from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'ipVanish proxy dictionary package'
LONG_DESCRIPTION = 'ipVanish proxy dictionary package which returns simple froxy dictionary given username and password'

setup(
    name='ipvanishproxy',
    version=VERSION,
    author='Nahom Dereje',
    author_email='dev@nahom.eu.org',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_dir={"":"app"},
    packages=[],
    install_requires=find_packages(),
    keywords=['IpVanish', "Proxy"],
    classifiers= [
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Education",
                "Programming Language :: Python :: 3",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: Microsoft :: Windows"
            ]
)