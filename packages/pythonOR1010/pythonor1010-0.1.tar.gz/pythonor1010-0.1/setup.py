from setuptools import setup, find_packages

setup(
    name='pythonOR1010',
    version='0.01',
    author='Adil Aziz',
    description='A package for outlier detection using the Interquartile Range (IQR) method',
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
)
