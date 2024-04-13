from setuptools import setup, find_packages

setup(
    name='rtrafactor',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'google',
    ],
    author='Udit Raj',
    author_email='udit_2312res708@iitp.ac.in',
    description='RTRA official library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/rtrafactor',
)
