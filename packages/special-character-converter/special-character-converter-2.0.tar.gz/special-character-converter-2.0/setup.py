from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='special-character-converter',
    version='2.0',
    description='Special Character Converter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Kunal',
    author_email='your.email@example.com',
    packages=find_packages(),
)
