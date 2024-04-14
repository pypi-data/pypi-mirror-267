from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='2.5',
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    description='Provides functionality to generate headlines from articles using natural language processing techniques.',
    long_description=open('README.md').read(),  # Read the contents of README.md
    long_description_content_type='text/markdown',  # Specify the content type of the l
    install_requires=[
        'requests',
        'nltk',
        'numpy',
        'scipy==1.12.0',
        'gensim',
        'networkx',
        'textacy',
        'transformers',
        'torch',
        'spacy'
    ],
    python_requires='>=3.6',
)