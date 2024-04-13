from setuptools import setup, find_packages


def readme():
    with open('../README.md', 'r') as f:
        return f.read()


setup(
    name='areacet',
    version='0.0.3',
    author='karleneg',
    author_email='kolya.gar.1@gmail.com',
    description='This is the simplest modul for calculate figure area.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/krimerkhex',
    packages=find_packages(),
    install_requires=['pytest==8.1.1', 'loguru==0.7.2'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='files areaDeterminant ',
    python_requires='>=3.11'
)
