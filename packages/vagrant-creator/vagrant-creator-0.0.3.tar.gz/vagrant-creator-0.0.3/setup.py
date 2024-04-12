from setuptools import setup, find_packages
import os

setup(
    name='vagrant-creator',
    version='0.0.3',
    author='Chandula Jayathilake',
    author_email='chandulaj3000@gmail.com',
    description='A tool to generate Vagrant init files with custom configurations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChandulaJ/vagrant-creator',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ],
    package_data={
        '': ['*.sh'],
    },
entry_points={
    'console_scripts': [
        'vagrant-creator = vagrant_creator.vagrant_creator:generate_vagrantfile'

    ],
},
    include_package_data=True,
    install_requires=[],
)

