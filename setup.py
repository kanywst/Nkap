import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def _requires_from_file(filename):
	return open(filename).read().splitlines()

setuptools.setup(
    name="Nkap",
    version="1.0.0",
    author="takuma",
    author_email="ta1234kuma@gmail.com",
    description="Nkap is a simple network reconnaissance tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kanywst/nkap",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['nkap = nkap.nkap:main']
    },
    python_requires='>=3.7',
)