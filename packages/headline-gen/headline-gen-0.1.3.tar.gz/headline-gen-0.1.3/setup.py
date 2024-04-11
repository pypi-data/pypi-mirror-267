from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='0.1.3',
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
