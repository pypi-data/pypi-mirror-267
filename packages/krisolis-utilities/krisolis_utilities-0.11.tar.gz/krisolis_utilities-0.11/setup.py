from setuptools import setup, find_packages

setup(
    name='krisolis_utilities',
    version='0.11',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn'
        # Add any other dependencies here
    ],
    author='Tehsein',
    description='Utility functions for data visualization and model evaluation',
    url='https://github.com/tfiroze/krisolis_utilities',
    keywords='krisolis utilities tools',

)
