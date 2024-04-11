from setuptools import setup, find_packages

setup(
    name='rtralm',
    version='0.2',
    author='Udit Raj',
    author_email='udit_2312res708@iitp.ac.in',
    description='Python library for RTRA (Retrieve, Transform, and Adapt) Connector using Hugging Face models',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['requests'],  # Add any dependencies here
)
