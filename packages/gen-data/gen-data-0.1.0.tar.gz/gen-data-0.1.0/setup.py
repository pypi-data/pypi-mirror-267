from setuptools import setup, find_packages

setup(
    name='gen-data',
    version='0.1.0',
    description='A tool to generate synthetic data from prompts',
    author='vivek kolasani',
    author_email='kolasaniv1996@gmail.com',
    packages=find_packages(),
    install_requires=[
        'transformers>=4.0.0',
        'torch>=1.7.0',
    ],
)
