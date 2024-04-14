from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='IsNumberEven',
    version='1.1.0',
    packages=find_packages(),
    description='Return true if the given number is even.',
    author='Thiago S Adriano',
    author_email='prof.thiagoadriano@gmail.com',
    url='https://github.com/programadriano/is-even',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown' 
)