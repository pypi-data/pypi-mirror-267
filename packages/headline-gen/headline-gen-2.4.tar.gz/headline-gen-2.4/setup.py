from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='2.4',
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    description='Provides functionality to generate headlines from articles using natural language processing techniques.',
    long_description=open('README.md').read(),  # Read the contents of README.md
    long_description_content_type='text/markdown',  # Specify the content type of the l
    install_requires=[
        'requests==2.31.0',
        'nltk==3.8.1',
        'numpy==1.26.4',
        'scipy==1.12.0',
        'gensim==4.3.2',
        'networkx==3.3',
        'textacy==0.13.0',
        'transformers==4.39.3',
        'torch==2.2.2',
        'spacy==3.7.4'
    ],
    python_requires='>=3.6',
)