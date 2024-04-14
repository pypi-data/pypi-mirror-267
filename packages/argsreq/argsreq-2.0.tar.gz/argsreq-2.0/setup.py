from setuptools import setup, find_packages

VERSION = '2.0'
DESCRIPTION = 'install all requirements'
LONG_DESCRIPTION = 'easy'
setup(
    name="argsreq",
    version=VERSION,
    author="akkam222",
    author_email="ahmedakkam@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={'colorls': ['config/colorls.toml']},
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
