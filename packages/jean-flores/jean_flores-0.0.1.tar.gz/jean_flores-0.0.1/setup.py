from setuptools import setup

r = open("./README.md", "r")

setup(

    name= 'jean_flores',
    packages= ['jean_flores'],
    version= '0.0.1',
    description= 'Trabajo de modulos',
    long_description= r.read(),
    long_description_content_type= 'text/markdown',
    author= 'CARLO_10',
    author_email= 'antonicontrerasaveiro@gmail.com',
    classifiers= [],
    license= 'MIT',
    include_package_data= True
)