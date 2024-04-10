from setuptools import setup, find_packages

setup(
    name='rtrapy',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Udit Raj',
    author_email='udit_2312res708@iitp.ac.in',
    description='Package for RTRAConnect functionality',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/uditakhourii/rtrapy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
