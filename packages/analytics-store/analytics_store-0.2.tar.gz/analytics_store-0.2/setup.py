from setuptools import setup, find_packages

setup(
    name='analytics_store',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn'
    ],
    author='Tehsein',
    description='Utility functions for data visualization and model evaluation',
    url='https://github.com/tfiroze/Analytics_Store'
)
