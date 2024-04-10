from setuptools import setup, find_packages

setup(
    name='HTLMSmall',
    version='0.1',
    packages=find_packages(),
    description='A Python library for connecting to RTRA (Retrieve, Transform, and Aggregate) services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Udit Raj',
    author_email='udit_2312res708@iitp.ac.in',
    url='https://github.com/uditakhourii/rtra-connector',
    license='MIT',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
