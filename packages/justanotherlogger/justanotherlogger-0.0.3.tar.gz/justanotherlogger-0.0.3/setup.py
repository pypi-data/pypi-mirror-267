from setuptools import find_packages, setup


setup(
    name='justanotherlogger',
    packages=find_packages(include=['justanotherlogger']),
    version='0.0.3',
    description='A very simple logger',
    long_description=open("README.md"),
    long_description_content_type="text/markdown",
    author='RockArtist33',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.1.1'],
    test_suite='testsuite'
)