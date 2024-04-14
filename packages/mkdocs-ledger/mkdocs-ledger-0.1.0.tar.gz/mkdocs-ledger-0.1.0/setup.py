from setuptools import setup, find_packages

setup(
    name='mkdocs-ledger',
    version='0.1.0',
    author='sjnscythe',
    author_email='scytheabhi97@gmail.com',
    description='poc for ledger',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sjnscythe',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
