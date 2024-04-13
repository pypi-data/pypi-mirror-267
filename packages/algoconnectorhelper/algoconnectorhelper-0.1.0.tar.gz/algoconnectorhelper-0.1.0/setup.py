from setuptools import setup, find_packages

setup(
    name='algoconnectorhelper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',  # Add any dependencies your package needs
        'jugaad_trader',
        'pyotp'
    ],
    # Add additional metadata here
    author='codingbeast',
    author_email='advrter@email.com',
    description='This package provides helper functions for algo trading.',
    url='https://github.com/codingbeast/algoConnectorHelper',
)
