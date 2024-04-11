from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='2.0',
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    install_requires=[
        'requests',
        'nltk',
        'numpy',
        'scipy',
        'gensim',
        'networkx',
        'textacy',
        'transformers',
        'torch'
    ],
    python_requires='>=3.6',
)
