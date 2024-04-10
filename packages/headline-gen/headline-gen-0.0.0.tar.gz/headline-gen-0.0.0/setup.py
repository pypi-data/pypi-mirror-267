from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='0.0.0',
    packages=find_packages(),
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    install_requires=['textacy', 'regex', 'transformers', 'nltk', 'torch', 'scipy', 'gensim'],
    python_requires='>=3.6',
)
