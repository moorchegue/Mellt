import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='mellt',
    version=open(os.path.join(here, 'VERSION')).readline().strip(),
    description='A brute force password checker that returns a meaningful '
                'number describing the real world strength of your password',
    long_description='See README.markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    author='ravisorg',
    url='https://github.com/ravisorg/Mellt',
    keywords='passwords',
    packages=find_packages(),
    py_modules=['mellt'],
    zip_safe=False,
    install_requires=[],
    test_suite="mellt",
    include_package_data=True,
    data_files=[('', ['common-passwords.txt'])]
)
