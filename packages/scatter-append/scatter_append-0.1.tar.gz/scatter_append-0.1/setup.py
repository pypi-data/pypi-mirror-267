from setuptools import setup, find_packages

setup(
    name='scatter-append',
    version='0.1',
    description='A utility for scatter appending to mutable sequences.',
    author='Rhys Newbury, Bryce Ferenczi',
    author_email='rhys.newbury@monash.edu, bryce.ferenczi@monash.edu',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
