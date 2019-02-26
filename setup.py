import setuptools
setuptools.setup(
    name="gesiel",
    version="0.1.4",
    url="https://github.com/gabrielweich/gesiel",
    author="Gabriel Weich",
    author_email="gabrielweich.dev@gmail.com",
    description="Simple and flexible schema definition.",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
