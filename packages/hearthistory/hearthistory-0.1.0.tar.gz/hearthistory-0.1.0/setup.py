from setuptools import setup, find_packages

setup(
    name='hearthistory',
    version='0.1.0',
    description='A library to generate random artworks from the Art Institute of Chicago',
    author='Kevin Song',
    author_email='kevinmsong@email.com',
    url='https://github.com/kevinmsong/ApplicationProgrammingInterfaces',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pillow'
    ],
    entry_points={
        'console_scripts': [
            'hearthistory = hearthistory.cli:main'
        ]
    }
)