from setuptools import setup, find_packages

setup(
    name='awil_ad9833',
    author='Noriki Mochizuki',
    author_email='noriki.mochizuki.mj@gmail.com',
    license='MIT',
    version='0.1.0',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'awil_ft232h' 
    ]
)
