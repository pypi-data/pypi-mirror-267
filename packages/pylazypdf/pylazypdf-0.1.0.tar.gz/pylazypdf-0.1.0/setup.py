from setuptools import setup, find_packages
import pylazypdf as plp

setup(
    name='pylazypdf',
    version=plp.version(),
    author='fullzer4',
    author_email='gabrielpelizzaro@gmail.com',
    description='Simplify your pdf automations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fullzer4/pylazypdf',
    packages=find_packages(),
    install_requires=[
        'maturin',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
