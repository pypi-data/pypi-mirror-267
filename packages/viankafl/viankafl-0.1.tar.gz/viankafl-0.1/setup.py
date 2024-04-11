from setuptools import setup

readme = open("./README.md", "r")

setup (

    name= 'viankafl',
    packages= ['pyvianka'],
    version= '0.1',
    description= 'Este es mi paquete pypi',
    long_description= readme.read(),
    long_description_content_type= 'text/markdown',
    author= 'vianka',
    author_email= 'vianka726@gmail.com',
    classifiers= [ ],
    license='MIT',
    include_package_data= True    
)