from setuptools import setup, find_packages

setup(
    name='headline-gen',
    version='0.0.2.2',
    packages=find_packages(),
    author='venkatchoudharyala',
    author_email='venkatchoudhary.ala@gmail.com',
    install_requires=['nltk', 'regex', 'textacy', 'gensim', 'transformers', 'scipy'],
    python_requires='>=3.6',
)