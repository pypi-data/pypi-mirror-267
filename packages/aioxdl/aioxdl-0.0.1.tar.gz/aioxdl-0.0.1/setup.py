from setuptools import setup, find_packages

with open("README.md", "r") as o:
    long_description = o.read()

DATA01 = "clintonabrahamc@gmail.com"

DATA02 = ['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules']
setup(
    name='aioxdl',
    license='MIT',
    zip_safe=False,
    version='0.0.1',
    classifiers=DATA02,
    author_email=DATA01,
    python_requires='~=3.9',
    packages=find_packages(),
    author='Clinton-Abraham',
    install_requires=['aiohttp'],
    long_description=long_description,
    description='python helper modules',
    url='https://github.com/Clinton-Abraham',
    keywords=['python', 'downloader', 'aiohttp'],
    long_description_content_type="text/markdown")
