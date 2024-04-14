from setuptools import setup, find_packages

setup(
    name='efriser',
    version='0.1.3',
    author='Douglas Ssekuwanda',
    author_email='cytixdoug@gmail.com',
    description='This is a python package to aid in fiscalisation of invoices with the Uganda Revenue Authority (URA) using the EFRIS API.',
    packages=find_packages(),
    install_requires=[
        'requests>=2.24.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)