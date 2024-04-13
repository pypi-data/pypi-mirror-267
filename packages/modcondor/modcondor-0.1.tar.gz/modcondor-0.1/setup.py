from setuptools import setup

read = open('./README.md', 'r')

setup(
    name='modcondor',
    packages =['modcondor'],
    version= '0.1',
    description= "Ejercicio de paquetes de python",
    long_description= read.read(),
    long_description_content_type= 'text/markdown',
    author='jhony',
    author_email= 'jhony28bravo@gmail.com',
    classifiers= [],
    license= 'MIT',
    include_package_data= True
)