"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup
import pathlib

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='chkpt',
    version='0.1.0',
    description='A tiny pipeline builder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/msuozzo/chkpt',
    author='Matthew Suozzo',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='pipeline, data, prototyping',
    py_modules=["chkpt"],
    python_requires='>=3.6, <4',
    install_requires=[],
    project_urls={
        'Bug Reports': 'https://github.com/msuozzo/chkpt/issues',
        'Source': 'https://github.com/msuozzo/chkpt/',
    },
)
