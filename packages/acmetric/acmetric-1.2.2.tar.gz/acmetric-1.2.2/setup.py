from setuptools import setup, find_packages

setup(
    name='acmetric',
    version='1.2.2',
    packages=find_packages(include=['acmetric', 'acmetric.*']),
    install_requires=[
        'cycler>=0.11.0',
        'seaborn>=0.11.2',
        'matplotlib>=3.5',
        'numpy>=1.20.0',
        'scipy>=1.7.0'
    ]
)
