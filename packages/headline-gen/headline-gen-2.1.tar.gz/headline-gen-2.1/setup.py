from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='2.1',
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
