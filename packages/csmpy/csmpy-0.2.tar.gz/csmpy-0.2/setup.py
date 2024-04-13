import setuptools

with open("README.md", "r") as pkg:
    long_description = pkg.read()

setuptools.setup(
    name='csmpy',
    version='0.2',
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML',
    ],
    author='Endormi',
    description='Color scheme manager package for your projects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/endormi/csm',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
