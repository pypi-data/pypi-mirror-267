from setuptools import setup, find_packages

setup(
    name='coreai-sdk',
    version='0.1.0',
    description='A simple Python package for cryptographic operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Moh Afrizal',
    author_email='moh.afrizal@bni.co.id',
    url='https://github.com/afrizalars98/coreai-sdk',
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'python-jose',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)
