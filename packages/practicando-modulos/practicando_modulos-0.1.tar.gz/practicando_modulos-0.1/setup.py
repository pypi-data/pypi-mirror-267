from setuptools import setup

readme = open('./README.md','r')

setup(
    name ='practicando_modulos',
    packages = ["practicando_modulos"],
    version ='0.1',
    description ='ejercicios con modulos',
    log_description = readme.read(),
    long_description_content_type= "text/markdown",
    author='Eddy Mamani Mamani',
    author_email='emamanimamani630@gmail.com',
    keywords = ['testing', 'logging', 'example'],
    classifiers=[],
    license = 'MIT',
    include_package_data = True
)
