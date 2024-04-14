import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='podRacer',
    version='0.0.1.2',
    author='Mike Afshari',
    author_email='theneed4swede@gmail.com',
    description='A library for interacting with podcasts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
