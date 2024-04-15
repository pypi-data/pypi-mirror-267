from setuptools import find_packages, setup

setup(
    name='shtwopy',
    packages=find_packages(include=['shtwopy']),
    version='0.1.0',
    description='Convert a python script into a decrypted shell script and vice versa.',
    author='Florian Grethler',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    license='GPL-3.0',
    url='https://github.com/grethler/sh2py',
    download_url='https://github.com/grethler/Sh2py/archive/refs/tags/0.1.0.tar.gz'
)
